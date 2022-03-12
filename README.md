# P(you)

Add a new dimension to password identification: **time**

This program uses machine learning to determine the validity of a user based on the timing of their keystrokes.

The algorithm is implemented through a deep-learning neural network of arbitrary depth, with optimization done using backpropogating gradient descent.

In order to increase accuracy, the program also implements a prior belief that the user is the correct person. This is done in 3 stages:

1. Test the network on (preffereably different from training) data, and generate normal distributions for user and non-user test outcomes. (The distribution is done on the log of the network outcome to fix scaling issues).
2. Use Bayes theorem with total probability to find P(User|R=log(r)) with R as the network outcome, and f(R|User) being the normal distributions generated in the previous steps.
3. If the Bayes output reaches a defined threshold probability, then the user passes:

Interestingly, if P(R=r|User) >> P(R=r|Non-User), this final function resembles another sigmoid function. This filter is particularly useful for dynamically tuning the program based on continued use/historical data without needing to update the neural network.

![Bayes process graphic](https://github.com/aklein4/P-you-/blob/master/images/bayes-prior-graphic.jpeg)

With test password "adam klein" (18 datwa points), 5 layer neural network, prior belief of correct user as 0.6, and an acceptance probability threshold of 0.5:

Based on 50 non-user human tests (blue - each graph is different person), the program identifies non-user humans with 88 percent accuracy.

Based on 50 user tests (green), the program identifies a correct user with 95 percent accuracy.

Based on 2000 tests with randomly generated inputs (orange, each graph is different random range), the program rejects randomly generated inputs with 95 percent accuracy.

Histograms of different user probabilities, with x axis representing P(User|R=r) where r is neural net prediction:

![testing graphic](https://github.com/aklein4/P-you-/blob/master/images/P-you-testing-outcomes.png)

**Training data:**
Maalej, A. (2020, November 15). EmoSurv: A typing biometric (Keystroke Dynamics) dataset with emotion labels created using computer keyboards. IEEE DataPort.
Retrieved February 25, 2022, from https://ieee-dataport.org/open-access/emosurv-typing-biometric-keystroke-dynamics-dataset-emotion-labels-created-using#files 
