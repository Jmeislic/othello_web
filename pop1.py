from stable_baselines3 import PPO
import pickle

model = PPO.load("ppo_12500000")

weights = {}
for k, v in model.policy.state_dict().items():
    weights[k] = v.cpu().numpy()

with open("othello_policy_numpy.pkl", "wb") as f:
    pickle.dump(weights, f)
