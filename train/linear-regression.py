import torch
import os

true_w = torch.tensor([2., -3.])
true_b = 4.


def create_data(w, b, size_datasets):
    x = torch.normal(0, 1., (size_datasets, len(w)))
    y = torch.matmul(x, w) + b
    y += torch.normal(0, 0.01, y.shape)
    return x, y.reshape(-1, 1)


class LinearNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(2, 1)

    def forward(self, x):
        y = self.linear(x)
        return y


class LinearNetModule(object):
    def __init__(self):
        self.net = LinearNet()
        self.loss = torch.nn.SmoothL1Loss()
        self.features, self.labels = create_data(true_w, true_b, 1000)
        self.ds_train = torch.utils.data.TensorDataset(
            self.features, self.labels)
        self.dl_train = torch.utils.data.DataLoader(
            self.ds_train, batch_size=10, shuffle=True)
        self.features_test, self.labels_test = create_data(true_w, true_b, 100)
        self.ds_test = torch.utils.data.TensorDataset(
            self.features_test, self.labels_test)
        self.dl_test = torch.utils.data.DataLoader(
            self.ds_test, batch_size=100, shuffle=True)

    def train(self, lr=0.01, epochs=100):
        optimizer = torch.optim.SGD(self.net.parameters(), lr=lr)
        for epoch in range(epochs):
            for x, y in self.dl_train:
                y_hat = self.net(x)
                loss = self.loss(y_hat, y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            loss_train = self.loss(self.net(self.ds_train[0][0]), self.ds_train[0][1])
            loss_test = self.loss(self.net(self.ds_test[0][0]), self.ds_test[0][1])
            print(f'epoch {epoch + 1}, train loss {loss_train}, test loss {loss_test:f}')
        w = self.net.linear.weight.data
        print(f'w的估计误差：{true_w - w.reshape(true_w.shape)}, '
              f'b的估计误差：{true_b - self.net.linear.bias.data}')

    def infer(self, x):
        return self.net(x)

    def save(self, path='linear.ckpt'):
        torch.save(self.net, path)

    def load(self, path='linear.ckpt'):
        self.net = torch.load(path)

    def to_onnx(self, path='linear.onnx'):
        torch.onnx.export(self.net, self.ds_test[0][0], path)


if __name__ == '__main__':
    linear_net = LinearNetModule()
    linear_net.train()
    ret = linear_net.infer(torch.tensor([3., 4.]))
    print(ret)
    linear_net.save(os.path.join(os.getcwd(), 'train', 'linear.ckpt'))
    linear_net.load(os.path.join(os.getcwd(), 'train', 'linear.ckpt'))
    linear_net.to_onnx(os.path.join(os.getcwd(), 'train', 'linear.onnx'))
