@torch.no_grad()
def predict(self, passage, source):
    sentences = [sent.strip() for sent in passage] if isinstance(passage, list) \
                else [sent.strip() for sent in sent_tokenize(passage) if len(sent) > 3]

    results = []
    for tmp in sentences:
        inputs = self.tokenizer(
            f"Premise: {source} Hypothesis: {tmp}",
            truncation=True,
            max_length=512,
            return_tensors="pt"
        ).to(self.device)  # move entire dict to device

        outputs = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=128
        )

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # If model returns a float string like "0.95"
        try:
            results.append(float(decoded))
        except ValueError:
            # Otherwise just keep the label text (like "entailment")
            results.append(decoded)

    return results