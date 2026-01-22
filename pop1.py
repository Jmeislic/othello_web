
import pickle
from sb3_contrib import MaskablePPO

model = MaskablePPO.load("ppo_25000000")



weights = {}
for k, v in model.policy.state_dict().items():
    weights[k] = v.cpu().numpy()

with open("othello_policy_numpy2.pkl", "wb") as f:
    pickle.dump(weights, f)
