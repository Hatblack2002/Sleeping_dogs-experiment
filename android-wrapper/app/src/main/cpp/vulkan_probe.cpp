#define VK_USE_PLATFORM_ANDROID_KHR
#include <jni.h>
#include <vulkan/vulkan.h>
#include <android/native_window.h>
#include <android/native_window_jni.h>
#include <cstdio>
#include <cstdarg>
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
           hasExtension(instanceExt, "VK_KHR_android_surface") ? "YES" : "NO",
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

extern "C" JNIEXPORT jstring JNICALL
Java_com_vertil_sleepingdogs_MainActivity_vulkanProbeSurface(JNIEnv* env, jclass, jobject javaSurface) {
    std::string report = "VULKAN ANDROID SURFACE PROBE\\n";
    ANativeWindow* window = ANativeWindow_fromSurface(env, javaSurface);
    if (!window) {
        append(report, "ANativeWindow_fromSurface: FAILED\\n");
        return env->NewStringUTF(report.c_str());
    }
    uint32_t count = 0;
    VkResult r = vkEnumerateInstanceExtensionProperties(nullptr, &count, nullptr);
    std::vector<VkExtensionProperties> extensions(count);
    if (r == VK_SUCCESS) r = vkEnumerateInstanceExtensionProperties(nullptr, &count, extensions.data());
    const bool surfaceExt = hasExtension(extensions, "VK_KHR_surface");
    const bool androidExt = hasExtension(extensions, "VK_KHR_android_surface");
    append(report, "VK_KHR_surface: %s\\nVK_KHR_android_surface: %s\\n",
           surfaceExt ? "YES" : "NO", androidExt ? "YES" : "NO");
    if (r != VK_SUCCESS || !surfaceExt || !androidExt) {
        append(report, "Required instance WSI extension unavailable; result=%d\\n", r);
        ANativeWindow_release(window);
        return env->NewStringUTF(report.c_str());
    }
    const char* enabled[] = {"VK_KHR_surface", "VK_KHR_android_surface"};
    VkApplicationInfo app{};
    app.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
    app.pApplicationName = "Sleeping Dogs Android WSI probe";
    app.apiVersion = VK_API_VERSION_1_0;
    VkInstanceCreateInfo ci{};
    ci.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    ci.pApplicationInfo = &app;
    ci.enabledExtensionCount = 2;
    ci.ppEnabledExtensionNames = enabled;
    VkInstance instance = VK_NULL_HANDLE;
    r = vkCreateInstance(&ci, nullptr, &instance);
    append(report, "vkCreateInstance with Android WSI: %d\\n", r);
    if (r != VK_SUCCESS) {
        ANativeWindow_release(window);
        return env->NewStringUTF(report.c_str());
    }
    auto createSurface = reinterpret_cast<PFN_vkCreateAndroidSurfaceKHR>(
        vkGetInstanceProcAddr(instance, "vkCreateAndroidSurfaceKHR"));
    auto destroySurface = reinterpret_cast<PFN_vkDestroySurfaceKHR>(
        vkGetInstanceProcAddr(instance, "vkDestroySurfaceKHR"));
    auto getPresent = reinterpret_cast<PFN_vkGetPhysicalDeviceSurfaceSupportKHR>(
        vkGetInstanceProcAddr(instance, "vkGetPhysicalDeviceSurfaceSupportKHR"));
    auto getCaps = reinterpret_cast<PFN_vkGetPhysicalDeviceSurfaceCapabilitiesKHR>(
        vkGetInstanceProcAddr(instance, "vkGetPhysicalDeviceSurfaceCapabilitiesKHR"));
    auto getFormats = reinterpret_cast<PFN_vkGetPhysicalDeviceSurfaceFormatsKHR>(
        vkGetInstanceProcAddr(instance, "vkGetPhysicalDeviceSurfaceFormatsKHR"));
    auto getModes = reinterpret_cast<PFN_vkGetPhysicalDeviceSurfacePresentModesKHR>(
        vkGetInstanceProcAddr(instance, "vkGetPhysicalDeviceSurfacePresentModesKHR"));
    VkAndroidSurfaceCreateInfoKHR sci{};
    sci.sType = VK_STRUCTURE_TYPE_ANDROID_SURFACE_CREATE_INFO_KHR;
    sci.window = window;
    VkSurfaceKHR surface = VK_NULL_HANDLE;
    r = createSurface ? createSurface(instance, &sci, nullptr, &surface) : VK_ERROR_EXTENSION_NOT_PRESENT;
    append(report, "vkCreateAndroidSurfaceKHR: %d\\n", r);
    uint32_t deviceCount = 0;
    if (r == VK_SUCCESS) r = vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);
    append(report, "Physical devices: %u (result %d)\\n", deviceCount, r);
    if (r == VK_SUCCESS && deviceCount) {
        std::vector<VkPhysicalDevice> devices(deviceCount);
        r = vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data());
        for (uint32_t i = 0; r == VK_SUCCESS && i < deviceCount; ++i) {
            VkPhysicalDeviceProperties props{};
            vkGetPhysicalDeviceProperties(devices[i], &props);
            uint32_t familyCount = 0;
            vkGetPhysicalDeviceQueueFamilyProperties(devices[i], &familyCount, nullptr);
            std::vector<VkQueueFamilyProperties> families(familyCount);
            vkGetPhysicalDeviceQueueFamilyProperties(devices[i], &familyCount, families.data());
            bool present = false, graphics = false;
            for (uint32_t q = 0; q < familyCount; ++q) {
                VkBool32 supported = VK_FALSE;
                if (getPresent && surface) getPresent(devices[i], q, surface, &supported);
                if (supported && (families[q].queueFlags & VK_QUEUE_GRAPHICS_BIT)) {
                    present = true; graphics = true;
                }
            }
            VkSurfaceCapabilitiesKHR caps{};
            VkResult cr = getCaps && surface ? getCaps(devices[i], surface, &caps) : VK_ERROR_EXTENSION_NOT_PRESENT;
            uint32_t formatCount = 0, modeCount = 0;
            VkResult fr = getFormats && surface ? getFormats(devices[i], surface, &formatCount, nullptr) : VK_ERROR_EXTENSION_NOT_PRESENT;
            VkResult mr = getModes && surface ? getModes(devices[i], surface, &modeCount, nullptr) : VK_ERROR_EXTENSION_NOT_PRESENT;
            append(report, "\\nGPU: %s\\nGraphics+present queue: %s\\nSurface caps: %d\\nFormats: %u (%d)\\nPresent modes: %u (%d)\\n",
                   props.deviceName, (present && graphics) ? "YES" : "NO", cr, formatCount, fr, modeCount, mr);
            if (cr == VK_SUCCESS)
                append(report, "Surface extent min/max: %ux%u / %ux%u\\n",
                       caps.minImageExtent.width, caps.minImageExtent.height,
                       caps.maxImageExtent.width, caps.maxImageExtent.height);
        }
    }
    if (surface && destroySurface) destroySurface(instance, surface, nullptr);
    vkDestroyInstance(instance, nullptr);
    ANativeWindow_release(window);
    append(report, "\\nWSI probe complete; no game renderer linked.");
    return env->NewStringUTF(report.c_str());
}
