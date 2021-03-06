# M.Tech Thesis: Performance Evaluation of Simultaneous Perturbation Methods for Simulation Optimization and Policy Learning

The objective is to implement SP methods on RL problems. 

For implementation of these problems, we are using two SP methods: SPSA and RDSA along with a neural network based function approximator. Further, we analyze these algorithms on common discrete and continuous control environments and compare performance with the popular REINFORCE algorithm. 

![image](https://github.com/monika58/Mtech-Thesis-Project/blob/master/RL%20problems.png)



The experimental studies show that SPSA i) is easy to implement ii) takes less time in training iii) requires two function measurements per iteration and iv) outperforms REINFORCE in walking robot task.

![cartpole](https://github.com/monika58/Mtech-Thesis-Project/blob/master/Learning_curve_cartpole.png)
![acrobot](https://github.com/monika58/Mtech-Thesis-Project/blob/master/Learning_curve_acrobot.png)
