import numpy as np
import matplotlib.pyplot as plt

# Pour charger MNIST ( excuter une seule fois)
from keras.datasets import mnist # ou utiliser fetch_openml si pas de Keras

np.random.seed(42)

# ====================== 1. INITIALISATION ======================
def initialize_parameters(layers_dims):
    """ layers_dims = [784, n_h1, n_h2, ..., 10] """
    parameters = {}
    L = len(layers_dims) - 1

    for l in range(1, L + 1):
        n_prev = layers_dims[l-1]
        n_current = layers_dims[l]
        parameters[f"W{l}"] = np.random.randn(n_current, n_prev) * 0.01
        parameters[f"b{l}"] = np.zeros((n_current, 1))

        assert parameters[f"W{l}"].shape == (n_current, n_prev)
        assert parameters[f"b{l}"].shape == (n_current, 1)

    return parameters


# ====================== 2. ACTIVATIONS ======================
def relu(Z):
    return np.maximum(0, Z)

def relu_derivative(Z):
    return Z > 0

def softmax(Z):
    """ Softmax numériquement stable : on soustrait le max pour éviter les overflow """
    Z_stable = Z - np.max(Z, axis=0, keepdims=True)
    exp_Z = np.exp(Z_stable)
    return exp_Z / np.sum(exp_Z, axis=0, keepdims=True)


# ====================== 3. FORWARD PROPAGATION ======================
def forward_propagation(X, parameters):
    """
    Forward propagation multi-couches.
    Dernière couche : softmax.
    """
    cache = {}
    A = X
    L = len(parameters) // 2

    for l in range(1, L):
        Z = np.dot(parameters[f"W{l}"], A) + parameters[f"b{l}"]
        A = relu(Z)
        cache[f"Z{l}"] = Z
        cache[f"A{l}"] = A

    # Dernière couche
    ZL = np.dot(parameters[f"W{L}"], A) + parameters[f"b{L}"]
    AL = softmax(ZL)

    cache[f"Z{L}"] = ZL
    cache[f"A{L}"] = AL
    return AL, cache


# ====================== 4. COUT ======================
def compute_cost(AL, Y):
    """ Categorical Cross-Entropy """
    m = Y.shape[1]
    cost = -np.sum(Y * np.log(AL + 1e-8)) / m
    return np.squeeze(cost)


# ====================== 5. BACKPROPAGATION ======================
def backward_propagation(X, Y, cache, parameters):
    """
    Backpropagation pour plusieurs couches.
    """
    grads = {}
    L = len(parameters) // 2
    m = Y.shape[1]
    AL = cache[f"A{L}"]

    dZ = AL - Y # Simplification pour softmax + cross-entropy

    for l in reversed(range(1, L + 1)):
        A_prev = X if l == 1 else cache[f"A{l-1}"]
        dW = (1/m) * np.dot(dZ, A_prev.T)
        db = (1/m) * np.sum(dZ, axis=1, keepdims=True)

        grads[f"dW{l}"] = dW
        grads[f"db{l}"] = db

        if l > 1:
            dA_prev = np.dot(parameters[f"W{l}"].T, dZ)
            dZ = dA_prev * relu_derivative(cache[f"Z{l-1}"])

    return grads


# ====================== 6. UPDATE ======================
def update_parameters(parameters, grads, learning_rate):
    L = len(parameters) // 2
    for l in range(1, L + 1):
        parameters[f"W{l}"] -= learning_rate * grads[f"dW{l}"]
        parameters[f"b{l}"] -= learning_rate * grads[f"db{l}"]
    return parameters


# ====================== 7. MODELE ======================
def model(X, Y, layers_dims, num_iterations=3000, learning_rate=0.15, print_cost=False):
    costs = []
    parameters = initialize_parameters(layers_dims)

    for i in range(num_iterations):
        AL, cache = forward_propagation(X, parameters)
        cost = compute_cost(AL, Y)
        grads = backward_propagation(X, Y, cache, parameters)
        parameters = update_parameters(parameters, grads, learning_rate)

        if i % 100 == 0:
            costs.append(cost)

        if print_cost and i % 500 == 0:
            print(f"Iteration {i:5d} | Cout = {cost:.6f}")

    return parameters, costs


# ====================== FONCTIONS AUXILIAIRES ======================
def predict(X, parameters):
    AL, _ = forward_propagation(X, parameters)
    return np.argmax(AL, axis=0)

def one_hot(Y, num_classes=10):
    return np.eye(num_classes)[Y].T


# ====================== CHARGEMENT DES DONNEES MNIST ======================
if __name__ == "__main__":
    # Chargement du vrai MNIST
    (X_train_raw, Y_train_raw), (X_test_raw, Y_test_raw) = mnist.load_data()

    # Aplatir les images 28x28  784
    X_train = X_train_raw.reshape(X_train_raw.shape[0], -1).T / 255.0
    X_test = X_test_raw.reshape(X_test_raw.shape[0], -1).T / 255.0

    # One-hot encoding
    Y_train = one_hot(Y_train_raw)
    Y_test = one_hot(Y_test_raw)

    print(f"X_train.shape = {X_train.shape}") # (784, 60000)
    print(f"Y_train.shape = {Y_train.shape}") # (10, 60000)
    print(f"X_test.shape = {X_test.shape}\n")

    # TODO : Definir plusieurs architectures et les tester
    architectures = [[784, 128, 10], [784, 256, 128, 10], [784, 512, 256, 128, 10]]

    results = {}

    for arch in architectures:
        arch_name = str(arch)
        print(f"\n{'='*50}")
        print(f"Architecture : {arch_name}")
        print(f"{'='*50}")

        parameters, costs = model(
            X_train, Y_train,
            layers_dims=arch,
            num_iterations=3000,
            learning_rate=0.15,
            print_cost=True
        )

        train_acc = np.mean(predict(X_train, parameters) == Y_train_raw) * 100
        test_acc  = np.mean(predict(X_test,  parameters) == Y_test_raw)  * 100

        print(f"\nAccuracy Train : {train_acc:.2f}%")
        print(f"Accuracy Test  : {test_acc:.2f}%")

        results[arch_name] = {"costs": costs, "train_acc": train_acc, "test_acc": test_acc}

    # Visualisation
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    for arch_name, res in results.items():
        iterations = [i * 100 for i in range(len(res["costs"]))]
        plt.plot(iterations, res["costs"], label=arch_name)
    plt.xlabel("Iterations")
    plt.ylabel("Cout (Cross-Entropy)")
    plt.title("Evolution du cout par architecture")
    plt.legend(fontsize=7)
    plt.grid(True)

    plt.subplot(1, 2, 2)
    arch_labels = [str(a) for a in architectures]
    test_accs   = [results[str(a)]["test_acc"]  for a in architectures]
    train_accs  = [results[str(a)]["train_acc"] for a in architectures]
    x = np.arange(len(arch_labels))
    width = 0.35
    plt.bar(x - width/2, train_accs, width, label="Train Accuracy")
    plt.bar(x + width/2, test_accs,  width, label="Test Accuracy")
    plt.xticks(x, [f"Arch {i+1}" for i in range(len(arch_labels))], rotation=15)
    plt.ylabel("Accuracy (%)")
    plt.title("Comparaison des accuracies")
    plt.legend()
    plt.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig("comparaison_architectures.png", dpi=150)
    plt.show()