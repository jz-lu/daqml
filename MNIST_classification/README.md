# MNIST classification

## Data Processing

Much of the learning code assumes there exists MNIST data at the root of this directory. This file location can be changed by changing `ROOT` in `binary_classifier`.

In order to correctly encode the MNIST data, we have included a jupyter notebook `prep_full.ipynb` to process and encode the data. To generate all possible digit pairings, we included `generate_binary_comparison.py`. Note in this case when running the binary classifier, we need to change the file names for the appropriate comparison. 

## Training binary classification models

In `binary_classifier.jl` we can train and test a binary classification model on the MNIST dataset.

---
## Julia Setup
This simulation was run using `Julia 1.7.1` and the included environment within `Manifest.toml` and `Project.toml`

---

### Required Inputs:

| Argument   | Description                                          | Type    | Default | 
|------------|------------------------------------------------------|---------|---------|
| `mode`     | Selects to train on digital or digital analog `DA` for digital analog `Digital` for digital  | String  | "DA"   |
| `depth`    | Number of layers (block depth)                       | Int     | -       |
| `noise`    | Train and test on noisy circuits if true             | Bool    | -       |
| `output`   | The directory to write the outputs of this program  | String  | "./"    |

### Optional Inputs:

| Argument   | Description                                           | Type     | Default |
|------------|-------------------------------------------------------|----------|---------|
| `--lr`     | Learning rate used for gradient descent               | Float64  | 0.1     |
| `--evo_time`| Evolution time parameter (only for digital analog)    | Float64  | 0.87    |

---

For optional arguments, we use a flag followed by the input, so if we wanted to change the evolution time we would have `--evo_time 0.80` for example.  

### Example command line argument

Run digital analog with number of layers = 2, and add noise
`julia binary_clean.jl DA 2 true ./`

Running digital analog with a changed evolution time
`julia binary_clean.jl DA 8 true ./ --evo_time 0.98`

### Output

At the end of the file, we save the training and test loss and accuracy for each training loop. We also save the parameters of the most recently trained circuit. 
