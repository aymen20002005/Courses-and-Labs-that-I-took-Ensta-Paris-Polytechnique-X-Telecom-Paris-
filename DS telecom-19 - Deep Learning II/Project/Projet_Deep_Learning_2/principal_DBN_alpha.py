import matplotlib.pyplot as plt
import numpy as np

from principal_RBM_alpha import RBM


class DBN:
    def __init__(self, config):

        self.config: tuple = config
        self.dbn: [RBM] = []
        for i in range(len(config) - 1):
            rbm = RBM(config[i], config[i + 1])
            self.dbn.append(rbm)

    def train_dbn(self, data, epochs=100, learning_rate=0.1, batch_size=100):
        for i in range(len(self.config) - 1):
            print("Pre-training RBM %d..." % i)
            self.dbn[i] = self.dbn[i].train_rbm(
                data=data,
                epochs=epochs,
                learning_rate=learning_rate,
                batch_size=batch_size,
            )

            data = np.random.binomial(1, self.dbn[i].entree_sortie_rbm(data))
        return self

    def generate_image_dbn(self, x_im, y_im, nb_data=1, nb_gibbs=100, plot=False):
        v = self.dbn[-1].generate_image_rbm(x_im, y_im, nb_data, nb_gibbs)
        for i in range(2, len(self.config)):
            v = np.random.binomial(1, self.dbn[-i].sortie_entree_rbm(v))

        images = v.reshape((nb_data, x_im, y_im))
        if plot:
            fig, axes = plt.subplots(1, nb_data, figsize=(10, 2))
            for i in range(nb_data):
                axes[i].imshow(images[i], cmap="gray")
                axes[i].axis("off")
            plt.suptitle(f"The config considered {self.config}")
            plt.show()
        return images
