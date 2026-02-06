#include <array>
#include <cstdio>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

std::string run_command(const std::string& cmd) {
    std::array<char, 256> buffer{};
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen failed");
    }
    while (fgets(buffer.data(), static_cast<int>(buffer.size()), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

int main(int argc, char* argv[]) {
    std::string metrics;
    std::string script;

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--metrics" && i + 1 < argc) {
            metrics = argv[++i];
        } else if (arg == "--python-script" && i + 1 < argc) {
            script = argv[++i];
        }
    }

    if (metrics.empty() || script.empty()) {
        std::cerr << "Usage: rdma_optimizer --metrics <path> --python-script <path>\n";
        return 1;
    }

    const std::string report_dir = "./reports/latest";
    const std::string cmd = "python3 " + script + " --input " + metrics + " --report " + report_dir;

    try {
        std::string output = run_command(cmd);
        std::cout << "[RDMA Optimizer] AI decision:\n" << output << std::endl;
        std::cout << "[RDMA Optimizer] Report generated at: " << report_dir << std::endl;
    } catch (const std::exception& ex) {
        std::cerr << "Execution failed: " << ex.what() << std::endl;
        return 2;
    }

    return 0;
}
