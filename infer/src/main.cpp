/*
 * @Author: Zhou Zijian 
 * @Date: 2024-03-01 23:26:45 
 * @Last Modified by: Zhou Zijian
 * @Last Modified time: 2024-03-01 23:51:49
 */

#include <memory>
#include "config.h"
#include "log.h"
#include "MNN/Interpreter.hpp"

int main(int argc, char *argv[])
{
    if (argc != 4) {
        LOGE("usage: %s model_path input_data_1 input_data_2", argv[0]);
        return -1;
    }
    
    std::shared_ptr<MNN::Interpreter> interpreter(MNN::Interpreter::createFromFile(argv[1]), MNN::Interpreter::destroy);
    MNN::ScheduleConfig config;
    config.type = MNN_FORWARD_CPU;
    config.numThread = 1;
    auto session = interpreter->createSession(config);
    auto inputTensor = interpreter->getSessionInput(session, nullptr);
    auto outputTensor = interpreter->getSessionOutput(session, nullptr);
    float *inputData = inputTensor->host<float>();
    inputData[0] = atof(argv[2]);
    inputData[1] = atof(argv[3]);
    interpreter->runSession(session);
    float *outputData = outputTensor->host<float>();
    LOGD("input: %f %f, output: %f", atof(argv[2]), atof(argv[3]), outputData[0]);
    interpreter->releaseSession(session);
    return 0;
}
