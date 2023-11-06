import math
import logging
import statistics
from   tqdm import tqdm
import torch
from   torch.utils.data import DataLoader, Dataset
import datasets
from   datasets import load_dataset
import transformers
from   transformers import DataCollatorForLanguageModeling


class BartPerplexityTester:
    def __init__(self, model, tokenizer, text, num_test_chars=None):
        self.model     = model
        self.tokenizer = tokenizer # bart-large is the same
        self.text = text

    def run_test(self, seq_len=None, num_test_chars=None, batch_size=8, mlm_prob=0.15):
        # Tokenize.  verbose=False elminates message 'token sequences too long for model'
        tok_ids = self.tokenizer(self.text, add_special_tokens=False, verbose=False).input_ids

        # Split into tokenized sequences all of the same length and discard any short samples at the end
        if seq_len is None:
            seq_len  = self.tokenizer.model_max_length
        samples = [c for c in chunk(tok_ids, seq_len) if len(c)==seq_len]
        print('Loaded {:,} samples of length {:,} tokens'.format(len(samples), len(samples[0])))

        # Add bos and eos tokens and create the decoder_input_ids
        # mask_token_id = 50264
        bos = self.tokenizer.bos_token_id               # = 0
        eos = self.tokenizer.eos_token_id               # = 2
        dst = self.model.config.decoder_start_token_id  # = 2 (same as eos token id)
        input_ids   = [[bos] + sample + [eos] for sample in samples]
        decoder_ids = [[dst] + iids[:-1]      for iids   in input_ids]  # shift_tokens_right

        # Put this all into a dataset and create the loader
        # The collator will take care of randomly masking the input_id tokens and creating the 
        # 'labels' keys with -100 for any non-masked token
        dataset    = EvalDataset(input_ids, decoder_ids)
        collator   = DataCollatorForLanguageModeling(tokenizer=self.tokenizer, mlm_probability=mlm_prob)
        dataloader = DataLoader(dataset, collate_fn=collator, batch_size=batch_size)

        # Run evaluation
        print('Testing')
        self.model.eval()
        losses = []
        for step, batch in enumerate(tqdm(dataloader, ncols=100, disable=False)):
            with torch.no_grad():
                torch.set_printoptions(threshold=10000, linewidth=150)
                decoder_ids = batch['decoder_input_ids']
                input_ids   = batch['input_ids']
                labels      = batch['labels']
                outputs = self.model(input_ids=input_ids, labels=labels, decoder_input_ids=decoder_ids)
            losses.append(outputs.loss.item())
        try:
            perplexity = math.exp(statistics.mean(losses))
        except OverflowError:
            perplexity = float('inf')
        return perplexity


# iterator to split a list into n segments
def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# Container for model data
class EvalDataset(Dataset):
    def __init__(self, input_ids, decoder_input_ids):
        assert len(input_ids) == len(decoder_input_ids)
        self.input_ids         = input_ids
        self.decoder_input_ids = decoder_input_ids

    def __getitem__(self, index):
        return {'input_ids':         self.input_ids[index],
                'decoder_input_ids': self.decoder_input_ids[index]}

    def __len__(self):
        return len(self.input_ids)