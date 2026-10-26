#include <jni.h>
#include <vulkan/vulkan.h>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

static void append(std::string& out, const char* fmt, ...) {
    char buffer[1024];
    va_list args;
    va_start(args, fmt);
    std::vsnprintf(buffer, sizeof(buffer), fmt, args);
    va_end(args);
    out += buffer;
}
static bool hasExtension(const std::vector<VkExtensionProperties>& list, const char* name) {
    for (const auto& e : list) if (std::strcmp(e.extensionName, name) == 0) return true;
    return false;
}
extern "C" JNIEXPORT jstring JNICALL
Java_com_vertil_sleepingdogs_MainActivity_vulkanProbe(JNIEnv* env, jclass) {
    std::string report;
    uint32_t loaderVersion = VK_API_VERSION_1_0;
    auto enumerateVersion = reinterpret_cast<PFN_vkEnumerateInstanceVersion>(
        vkGetInstanceProcAddr(VK_NULL_HANDLE, "vkEnumerateInstanceVersion"));
    if (enumerateVersion && enumerateVersion(&loaderVersion) != VK_SUCCESS) loaderVersion = VK_API_VERSION_1_0;
    append(report, "VULKAN NATIVE PROBE\nLoader API: %u.%u.%u\n",
           VK_VERSION_MAJOR(loaderVersion), VK_VERSION_MINOR(loaderVersion), VK_VERSION_PATCH(loaderVersion));
    uint32_t extCount = 0;
    VkResult r = vkEnumerateInstanceExtensionProperties(nullptr, &extCount, nullptr);
    if (r != VK_SUCCESS) {
        append(report, "Instance extension query failed: %d\n", r);
        return env->NewStringUTF(report.c_str());
    }
    std::vector<VkExtensionProperties> instanceExt(extCount);
    r = vkEnumerateInstanceExtensionProperties(nullptr, &extCount, instanceExt.data());
    if (r != VK_SUCCESS) {
        append(report, "Instance extension enumeration failed: %d\n", r);
        return env->NewStringUTF(report.c_str());
    }
    append(report, "Android surface: %s\nDebug utils: %s\n",
           hasExtension(instanceExt, VK_KHR_ANDROID_SURFACE_EXTENSION_NAME) ? "YES" : "NO",
           hasExtension(instanceExt, VK_EXT_DEBUG_UTILS_EXTENSION_NAME) ? "YES" : "NO");
    VkApplicationInfo app{VK_STRUCTURE_TYPE_APPLICATION_INFO};
    app.pApplicationName = "Sleeping Dogs Native Lab";
    app.applicationVersion = 1;
    app.pEngineName = "Native ARM64 Vulkan bring-up";
    app.engineVersion = 1;
    app.apiVersion = VK_API_VERSION_1_0;
    VkInstanceCreateInfo ci{VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO};
    ci.pApplicationInfo = &app;
    VkInstance instance = VK_NULL_HANDLE;
    r = vkCreateInstance(&ci, nullptr, &instance);
    append(report, "vkCreateInstance: %d\n", r);
    if (r != VK_SUCCESS) return env->NewStringUTF(report.c_str());
    uint32_t deviceCount = 0;
    r = vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);
    append(report, "Physical device query: %d; count: %u\n", r, deviceCount);
    if (r == VK_SUCCESS && deviceCount > 0) {
        std::vector<VkPhysicalDevice> devices(deviceCount);
        r = vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data());
        for (uint32_t i = 0; r == VK_SUCCESS && i < deviceCount; ++i) {
            VkPhysicalDeviceProperties props{};
            vkGetPhysicalDeviceProperties(devices[i], &props);
            uint32_t devExtCount = 0;
            vkEnumerateDeviceExtensionProperties(devices[i], nullptr, &devExtCount, nullptr);
            std::vector<VkExtensionProperties> devExt(devExtCount);
            if (devExtCount) vkEnumerateDeviceExtensionProperties(devices[i], nullptr, &devExtCount, devExt.data());
            VkPhysicalDeviceFeatures features{};
            vkGetPhysicalDeviceFeatures(devices[i], &features);
            append(report, "\nGPU %u: %s\nVendor ID: 0x%04x; Device ID: 0x%04x\nAPI: %u.%u.%u\n",
                   i, props.deviceName, props.vendorID, props.deviceID,
                   VK_VERSION_MAJOR(props.apiVersion), VK_VERSION_MINOR(props.apiVersion), VK_VERSION_PATCH(props.apiVersion));
            append(report, "Type: %u; driverVersion: %u\nExtensions: %u\n",
                   static_cast<unsigned>(props.deviceType), props.driverVersion, devExtCount);
            append(report, "robustBufferAccess: %s\nshaderClipDistance: %s\n",
                   features.robustBufferAccess ? "YES" : "NO",
                   features.shaderClipDistance ? "YES" : "NO");
            append(report, "VK_EXT_robustness2: %s\nVK_KHR_swapchain: %s\n",
                   hasExtension(devExt, "VK_EXT_robustness2") ? "YES" : "NO",
                   hasExtension(devExt, VK_KHR_SWAPCHAIN_EXTENSION_NAME) ? "YES" : "NO");
        }
    }
    vkDestroyInstance(instance, nullptr);
    append(report, "\nProbe complete. This checks Vulkan enumeration only; no game renderer is linked.");
    return env->NewStringUTF(report.c_str());
}
