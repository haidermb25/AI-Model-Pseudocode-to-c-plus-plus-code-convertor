import streamlit as st
import torch
import torch.nn as nn
import json
import math

# Load vocabulary
with open("vocabulary.json", "r") as f:
    vocab = json.load(f)

# Page Config
st.set_page_config(page_title="AI Pseudocode to Code Translator", layout="wide")

# Updated Dark Blue Theme Styling
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #0B192C;
        color: #ffffff;
    }
    .stTextArea textarea, .stTextInput input, .stCode, .stButton button {
        background-color: #1E2A3A;
        color: #ffffff;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #0b5ed7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Transformer Configuration
class Config:
    vocab_size = 12388
    max_length = 100
    embed_dim = 256
    num_heads = 8
    num_layers = 2
    feedforward_dim = 512
    dropout = 0.1
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

config = Config()

# Positional Encoding
class PositionalEncoding(nn.Module):
    def __init__(self, embed_dim, max_len=100):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, embed_dim)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-math.log(10000.0) / embed_dim))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.pe = pe.unsqueeze(0)

    def forward(self, x):
        return x + self.pe[:, :x.size(1)].to(x.device)

# Transformer Model
class Seq2SeqTransformer(nn.Module):
    def __init__(self, config):
        super(Seq2SeqTransformer, self).__init__()
        self.embedding = nn.Embedding(config.vocab_size, config.embed_dim)
        self.positional_encoding = PositionalEncoding(config.embed_dim, config.max_length)
        self.transformer = nn.Transformer(
            d_model=config.embed_dim,
            nhead=config.num_heads,
            num_encoder_layers=config.num_layers,
            num_decoder_layers=config.num_layers,
            dim_feedforward=config.feedforward_dim,
            dropout=config.dropout
        )
        self.fc_out = nn.Linear(config.embed_dim, config.vocab_size)

    def forward(self, src, tgt):
        src_emb = self.embedding(src) * math.sqrt(config.embed_dim)
        tgt_emb = self.embedding(tgt) * math.sqrt(config.embed_dim)
        src_emb = self.positional_encoding(src_emb)
        tgt_emb = self.positional_encoding(tgt_emb)
        out = self.transformer(src_emb.permute(1, 0, 2), tgt_emb.permute(1, 0, 2))
        out = self.fc_out(out.permute(1, 0, 2))
        return out

# Load Models
@st.cache_resource
def load_model(path):
    model = Seq2SeqTransformer(config).to(config.device)
    model.load_state_dict(torch.load(path, map_location=config.device))
    model.eval()
    return model

pseudo_to_cpp_model = load_model("transformer_epoch_1.pth")

# Translation Function
# Translation Function (Updated)
def translate(model, input_tokens, vocab, device, max_length=50):
    model.eval()
    input_ids = [vocab.get(token, vocab["<unk>"]) for token in input_tokens]
    input_tensor = torch.tensor(input_ids, dtype=torch.long).unsqueeze(0).to(device)
    output_ids = [vocab["<start>"]]

    for _ in range(max_length):
        output_tensor = torch.tensor(output_ids, dtype=torch.long).unsqueeze(0).to(device)
        with torch.no_grad():
            predictions = model(input_tensor, output_tensor)
        next_token_id = predictions.argmax(dim=-1)[:, -1].item()
        
        if next_token_id == vocab["<end>"]:
            break  # Stop generating when <end> token is reached
        
        output_ids.append(next_token_id)

    id_to_token = {idx: token for token, idx in vocab.items()}
    generated_tokens = [id_to_token.get(idx, "<unk>") for idx in output_ids[1:]]
    
    return " ".join(generated_tokens)  # Return translated code without <end> token

# Streamlit UI
st.title("🧠 Pseudocode to Code Translator")
st.write("Translate your pseudocode into real code with ease!")

user_input = st.text_area("📝 Enter your pseudocode below:", height=200)

if st.button("Translate to Code 🛠️"):
    tokens = user_input.strip().split()
    translated_code = translate(pseudo_to_cpp_model, tokens, vocab, config.device)
    st.subheader("🚀 Generated Code:")
    st.code(translated_code, language="cpp")

st.markdown("---")
st.caption("Built with Streamlit, PyTorch, and ❤️")
