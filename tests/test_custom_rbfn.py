import unittest
import numpy as np
from src.models.custom_rbfn import RadialBasisFunctionNetwork

class TestCustomRBFN(unittest.TestCase):
    def setUp(self):
        # Create a simple synthetic regression problem
        np.random.seed(42)
        self.X = np.random.normal(0, 1, (100, 5))
        # target = sum(X) + some noise
        self.y = np.sum(self.X, axis=1) + np.random.normal(0, 0.1, 100)
        
        self.model = RadialBasisFunctionNetwork(n_centers=10, gamma='scale', alpha=0.1, random_state=42)

    def test_fit_and_predict(self):
        # Fit model
        self.model.fit(self.X, self.y)
        
        # Check fitted attributes
        self.assertIsNotNone(self.model.centers_)
        self.assertEqual(len(self.model.centers_), 10)
        self.assertIsNotNone(self.model.gamma_)
        self.assertTrue(self.model.gamma_ > 0)
        
        # Predict on same data
        predictions = self.model.predict(self.X)
        self.assertEqual(predictions.shape, (100,))
        
        # Test predictions are reasonably close to true values (check R2 locally)
        ssr = np.sum((self.y - predictions) ** 2)
        sst = np.sum((self.y - np.mean(self.y)) ** 2)
        r2 = 1.0 - (ssr / sst)
        self.assertGreater(r2, 0.7)  # RBFN should capture this simple linear trend easily

    def test_insufficient_samples(self):
        # If n_samples < n_centers, it should adjust centers count gracefully
        small_X = self.X[:5]
        small_y = self.y[:5]
        
        model_small = RadialBasisFunctionNetwork(n_centers=10, gamma='scale')
        model_small.fit(small_X, small_y)
        
        self.assertEqual(len(model_small.centers_), 5)

if __name__ == '__main__':
    unittest.main()
