import numpy as np
import pickle
import copy
import gym
import matplotlib.pyplot as plt
import time
from gym import wrappers

def sigmoid(inpt):
    return 1.0 / (1 + np.exp(-1 * inpt))


def leaky_relu(x):
    #result = inpt
    #result[inpt < 0] = 0.01*inpt
    leaky_way1 = np.where(x > 0, x, x * 0.01)
    return leaky_way1

def relu(inpt):
    result = inpt
    result[inpt < 0] = 0
    return result


def softmax(x):
    f = np.exp(x - np.max(x))  # shift values
    return f / f.sum(axis=0)


def normalize(X):
    X -= np.mean(X, axis=0)
    X /= np.std(X, axis=0)
    return X


def train_network(weights, envv, activation="sigmoid"):
    episodic_rewards = 0
    data_inputs = envv.reset()
    #print(data_inputs)
    # print(data_inputs)
    state = data_inputs
    #state -= np.mean(state, axis=0)
    #state /= np.std(state, axis=0)
    #state = normalize(state)
    done = False
    while not done:
        r1 = []
        r1 = np.expand_dims(np.append(normalize(state),1), axis=0)
        for idx in range(len(weights) - 1):
            curr_weights = weights[idx]
            r1 = np.matmul(r1, curr_weights)
            r1 = drop_out(0.5,r1)
            if activation == "relu":
                r1 = leaky_relu(r1)
            elif activation == "sigmoid":
                r1 = sigmoid(r1)
        curr_weights = weights[-1]
        r1 = np.matmul(r1, curr_weights)
        r1 = softmax(r1[0])
        predicted_label = np.random.choice(2, 1, p=r1)
        next_state, reward, done, info = envv.step(predicted_label[0])
        state = next_state
        episodic_rewards = episodic_rewards+ reward
    return episodic_rewards


def delta(var, algo, epsilon):
    delta1 = []
    for i in range(len(var)):
        if algo == "uniform":
            d = 2 * np.round(np.random.uniform(0,1,(var[i].shape[0], var[i].shape[1]))) - 1
            delta1.append(d)
        else:
            d= np.random.uniform(0,1,(var[i].shape[0], var[i].shape[1]))
            for k in range(len(d)):
                for j in range(len(d[k])):
                    if d[k][j]<((1+epsilon)/(2+epsilon)):
                        d[k][j]=-1
                    else:
                        d[k][j]=1+epsilon
            delta1.append(d)
    return delta1


def perturb_weights(var, delta2, ck):
    var1 = []
    for i in range(len(var)):
        v = var[i] + ck * delta2[i]
        var1.append(v)
    return var1

'''
def soft_updates(delta2, ck, diff):
    g = []
    for i in range(len(delta2)):
        g1=diff / (2 * ck * delta2[i])
        g.append(g1)
    return g
'''

def update_weights(var, delta2, ck, diff, epsilon, algo):
    var2 = []
    for i in range(len(var)):
        if algo == "uniform" :
            v = var[i] + 3 * diff * delta2[i] / (2 * ck )
        else:
            v = var[i] + diff*delta2[i]/ (2 * ck *(1+epsilon))
        var2.append(v)
    return var2


def weight_initialization(input_shape,HL1_neurons, output_neurons, init_type):
    input_HL1_weights=[]
    HL2_output_weights = []
    if (init_type == "xavier"):
        input_HL1_weights = np.random.randn(input_shape, HL1_neurons)/np.sqrt(input_shape / 2.)
        HL2_output_weights = np.random.randn(HL1_neurons, output_neurons)/np.sqrt(HL1_neurons / 2.)
        #weights = np.array([input_HL1_weights, HL2_output_weights])
    elif(init_type =="uniform"):
        input_HL1_weights = np.random.uniform(low=-0.1, high=0.1,
                                              size=(input_shape, HL1_neurons))/np.sqrt(input_shape / 2.)
        HL2_output_weights = np.random.uniform(low=-0.1, high=0.1, size=(HL1_neurons, output_neurons))/np.sqrt(HL1_neurons / 2.)
    weights = np.array([input_HL1_weights, HL2_output_weights])
    #b1 = np.zeros((1, H))
    #b2 = np.zeros((1, H))
    return weights

def drop_out(p,h1):
    u1 = np.random.binomial(1, p, size=h1.shape)
    h1 *= u1
    return h1




# delta(numpy.array(input_HL1_weights),1)

#input_HL1_weights = np.random.uniform(low=-0.1, high=0.1,
#                                      size=(4, HL1_neurons))
# HL2_neurons = 10
# HL1_HL2_weights = np.random.uniform(low=-0.1, high=0.1,
#                                       size=(HL1_neurons, HL2_neurons))
#output_neurons = 2
#HL2_output_weights = np.random.uniform(low=-0.1, high=0.1, size=(HL1_neurons, output_neurons))
# weights = np.array([input_HL1_weights,
#                      HL1_HL2_weights,
#                     HL2_output_weights])

# HL1_neurons = 10
# input_HL1_weights = np.random.randn(4, HL1_neurons)
# HL2_neurons = 10
# HL1_HL2_weights = np.random.randn(low=-0.1, high=0.1,
#                                      size=(HL1_neurons, HL2_neurons))
# output_neurons = 2
# HL2_output_weights = np.random.randn(HL1_neurons, output_neurons)
#weights = np.array([input_HL1_weights,
                    # HL1_HL2_weights,
#                    HL2_output_weights])


#weights_old = weights
#tau = 0.5
start = time.time()
N = 5000
final_weights = []
final_rewards = []
replications = 1
env = gym.make("CartPole-v0")
env.seed(1)
algo = "nonuniform"
epsilon = 0.01

for j in range(replications):
    #np.random.seed(0)
    input_shape = 5
    output_dim = 2

    env1 = copy.deepcopy(env)
    env2 = copy.deepcopy(env)
    env3 = copy.deepcopy(env)
    # num_episodes = 5
    # alpha = 0.602
    # gamma = 0.101
    # a = 0.16
    # c = 1
    # A = 100
    a = 1.0
    c = 1.9
    A = 50
    N = 2000
    alpha = 1
    gamma = 1 / 6
    seed = 5
    discount_factor = 0.995
    HL1_neurons = 10
    weights = weight_initialization(input_shape, HL1_neurons, output_dim, "xavier")
    #print("weights= ", weights)
    rewards = []
    rewards_plus = []
    rewards_minus = []
    mean_rewards = []
    episode_id = 1
    env3 = wrappers.Monitor(env3, './cp_video2+ str(time.time()) + /',resume=True, video_callable=lambda episode_id: True,force=True)
    for i in range(N):
    #print(i)
        ak = a / (i + 1+A) ** alpha
        ck = c / (i + 1) ** gamma
    # delta = np.random.choice([1,-1],p = [0.5,0.5],size = total_elem)
        delta2 = delta(weights,"uniform",0)
        #print("delta = ", delta2)
        weights_plus = perturb_weights(weights, delta2, ck)
        weights_minus = perturb_weights(weights, delta2, -ck)

    # X1=env.reset()
    # X2 = env1.reset()
        rewplus = train_network(weights_plus, env1, activation="sigmoid")
        rewminus = train_network(weights_minus, env2, activation="sigmoid")
        rewards1 = train_network(weights, env3, activation="sigmoid")
        rewards.append(rewards1)
        m = np.mean(rewards[:-10])
        if m >195:
            break
        mean_rewards.append(m)
        rewards_plus.append(rewplus)
        rewards_minus.append(rewminus)
    #print("rewplus")
    #print(rewplus)
    #print("rewminus")
    #print(rewminus)
        print('rep = ',j,'episode =' ,i, 'reward = ',rewards1)
        diff = (rewplus - rewminus) * ak
        weights = update_weights(weights, delta2, ck, diff,epsilon, algo)
    final_rewards.append(rewards)
    env3.close()
    #for i in range(len(weights)):
    #    weights[i] = tau*weights_old[i] + (1-tau) * weights[i]
    #weights_old = weights
    #tau = 0.5
np.save('rdsa_ab_wgt_cp',weights)



avg_reward = np.zeros(N)
for i in range(N):
    sum = 0
    for k in range(len(final_rewards)):
        sum = sum + final_rewards[k][i]
    avg_reward[i]=sum/len(final_rewards)

avg_reward1=np.zeros(10)

avg_reward=np.load('cartpole_avg_rew_rdsa_u.npy')


for i in range(1000):
    if i%100 == 0:
        avg_reward1[int(i/100)]=avg_reward[i]
    #for k in range(len(final_rewards)):
    #    sum = sum + final_rewards[k][i]
    #avg_reward[i]=sum/len(final_rewards)

plt.plot(avg_reward1,'b')

np.save('cartpole_avg_rew_rdsa_u',final_rewards)

plt.plot(avg_reward,'b')





end = time.time()
print(end - start)

test_rewards=[]
for i in range(100):
    env3 = gym.make("CartPole-v0")
    rewards3 = train_network(weights, env3, activation="sigmoid")
    test_rewards.append(rewards3)
plt.plot(np.arange(100),test_rewards)








plt.plot(np.arange(N),rewards_plus)
plt.plot(np.arange(N),mean_rewards)
plt.plot(np.arange(N),rewards)
np.save('mr',mean_rewards)
np.save('rp',rewards_plus)
np.save('rm',rewards_minus)
np.save('r',rewards)
smoothed_rewards = [np.mean(avg_reward[max(0,i-50):i+1]) for i in range(len(avg_reward))]
smoothed_rewards1 = [np.mean(rewards[i-10:i+1]) for i in range(len(test_rewards))]

plt.figure(figsize=(12,8))
#plt.plot(smoothed_rewards1)
plt.plot(smoothed_rewards, 'b')
plt.title('SPSA based Policy Optimization')
plt.xlabel('Number of Episodes')
plt.ylabel('Smoothed Mean Rewards of last 10 episodes')
plt.show()



plt.figure(figsize=(12,8))
plt.plot(smoothed_rewards,'r')
#plt.plot(np.arange(N),rewards,'b')
plt.title('SPSA based Policy Optimization')
plt.xlabel('Number of Episodes')
plt.ylabel('Episodic reward')
plt.show()














''''
best yet configuration
--xavier
--a = 1
c = 1.9
A = 50
N = 1000
alpha = 1
gamma = 1/6
seed = 5
HL1_neurons = 10
sigmoid

or

a = 2.0
c = 2.5
A = 50
N = 2000
alpha = 1
gamma = 1/6
seed = 5
discount_factor = 0.995
HL1_neurons = 10



'''



