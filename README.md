# AI-Model-Pseudocode-to-c-plus-plus-code-convertor

A Transformer-based deep learning model that converts pseudocode into C++ code. The project is built using PyTorch and provides an interactive interface through Streamlit.

## Features

* Transformer-based Seq2Seq model
* Positional Encoding
* Streamlit web application
* Automatic code generation
* GPU support (CUDA)

## Technologies Used

* Python
* PyTorch
* Streamlit
* JSON

## Project Structure

```text
AI-Model-Pseudocode-to-c-plus-plus-code-convertor
│
├── app.py
├── vocabulary.json
├── transformer_epoch_1.pth
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/haidermb25/AI-Model-Pseudocode-to-c-plus-plus-code-convertor.git
```

Move into the project directory:

```bash
cd AI-Model-Pseudocode-to-c-plus-plus-code-convertor
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

## Example

Input pseudocode:

```text
START
READ a
READ b
sum = a + b
PRINT sum
END
```

Generated C++ code:

```cpp
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a;
    cin >> b;

    int sum = a + b;
    cout << sum;

    return 0;
}
```

## Future Improvements

* Support multiple programming languages
* Improve model accuracy
* Add syntax highlighting
* Allow code download

## Author

Ali Haider

* Software Engineer
* AI and Machine Learning Enthusiast

GitHub: https://github.com/haidermb25
