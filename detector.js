/**
 * Browser Fingerprinting Detection Module
 * Captures API invocations from fingerprinting attempts
 * Compatible with Chromium and Firefox browsers
 */

(function() {
    'use strict';
    
    // Storage for captured fingerprinting data
    window.fingerprintData = {
        canvas: [],
        webgl: [],
        audio: [],
        fonts: [],
        plugins: [],
        navigator: [],
        screen: [],
        storage: [],
        webrtc: [],
        battery: [],
        sensors: [],
        timing: [],
        hardware: [],
        other: []
    };

    // Timestamp of script initialization
    window.detectionStartTime = Date.now();

    // Helper function to log API calls
    function logAPICall(category, method, value) {
        const timestamp = Date.now() - window.detectionStartTime;
        const entry = {
            timestamp: timestamp,
            method: method,
            value: value,
            stackTrace: new Error().stack
        };
        
        if (window.fingerprintData[category]) {
            window.fingerprintData[category].push(entry);
        } else {
            window.fingerprintData.other.push(entry);
        }
    }

    // ============================================
    // CANVAS FINGERPRINTING DETECTION
    // ============================================
    if (CanvasRenderingContext2D.prototype.fillText) {
        const originalFillText = CanvasRenderingContext2D.prototype.fillText;
        CanvasRenderingContext2D.prototype.fillText = function(...args) {
            logAPICall('canvas', 'fillText', args[0]);
            return originalFillText.apply(this, args);
        };
    }

    if (CanvasRenderingContext2D.prototype.strokeText) {
        const originalStrokeText = CanvasRenderingContext2D.prototype.strokeText;
        CanvasRenderingContext2D.prototype.strokeText = function(...args) {
            logAPICall('canvas', 'strokeText', args[0]);
            return originalStrokeText.apply(this, args);
        };
    }

    if (HTMLCanvasElement.prototype.toDataURL) {
        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function(...args) {
            const result = originalToDataURL.apply(this, args);
            logAPICall('canvas', 'toDataURL', result.substring(0, 100) + '...');
            return result;
        };
    }

    if (HTMLCanvasElement.prototype.toBlob) {
        const originalToBlob = HTMLCanvasElement.prototype.toBlob;
        HTMLCanvasElement.prototype.toBlob = function(...args) {
            logAPICall('canvas', 'toBlob', 'called');
            return originalToBlob.apply(this, args);
        };
    }

    // ============================================
    // WEBGL FINGERPRINTING DETECTION
    // ============================================
    if (WebGLRenderingContext.prototype.getParameter) {
        const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(param) {
            const result = originalGetParameter.apply(this, arguments);
            logAPICall('webgl', 'getParameter', { param: param, result: result });
            return result;
        };
    }

    if (typeof WebGL2RenderingContext !== 'undefined' && WebGL2RenderingContext.prototype.getParameter) {
        const originalGetParameter2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = function(param) {
            const result = originalGetParameter2.apply(this, arguments);
            logAPICall('webgl', 'getParameter', { param: param, result: result });
            return result;
        };
    }

    if (WebGLRenderingContext.prototype.getExtension) {
        const originalGetExtension = WebGLRenderingContext.prototype.getExtension;
        WebGLRenderingContext.prototype.getExtension = function(name) {
            const result = originalGetExtension.apply(this, arguments);
            logAPICall('webgl', 'getExtension', name);
            return result;
        };
    }

    // ============================================
    // AUDIO FINGERPRINTING DETECTION
    // ============================================
    if (typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined') {
        const AudioContextConstructor = window.AudioContext || window.webkitAudioContext;
        const originalCreateOscillator = AudioContextConstructor.prototype.createOscillator;
        AudioContextConstructor.prototype.createOscillator = function() {
            logAPICall('audio', 'createOscillator', 'called');
            return originalCreateOscillator.apply(this, arguments);
        };

        const originalCreateAnalyser = AudioContextConstructor.prototype.createAnalyser;
        AudioContextConstructor.prototype.createAnalyser = function() {
            logAPICall('audio', 'createAnalyser', 'called');
            return originalCreateAnalyser.apply(this, arguments);
        };
    }

    if (typeof AnalyserNode !== 'undefined' && AnalyserNode.prototype.getFloatFrequencyData) {
        const originalGetFloatFrequencyData = AnalyserNode.prototype.getFloatFrequencyData;
        AnalyserNode.prototype.getFloatFrequencyData = function(array) {
            logAPICall('audio', 'getFloatFrequencyData', array.length);
            return originalGetFloatFrequencyData.apply(this, arguments);
        };
    }

    // ============================================
    // FONT ENUMERATION DETECTION
    // ============================================
    if (document.fonts && document.fonts.check) {
        const originalCheck = document.fonts.check;
        document.fonts.check = function(font) {
            logAPICall('fonts', 'check', font);
            return originalCheck.apply(this, arguments);
        };
    }

    // ============================================
    // NAVIGATOR PROPERTIES DETECTION
    // ============================================
    const navigatorProps = [
        'userAgent', 'platform', 'language', 'languages', 'hardwareConcurrency',
        'deviceMemory', 'maxTouchPoints', 'vendor', 'vendorSub', 'productSub',
        'oscpu', 'appVersion', 'appName', 'appCodeName', 'doNotTrack'
    ];

    navigatorProps.forEach(prop => {
        if (prop in navigator) {
            try {
                const descriptor = Object.getOwnPropertyDescriptor(Navigator.prototype, prop) ||
                                 Object.getOwnPropertyDescriptor(navigator, prop);
                if (descriptor && descriptor.get) {
                    const originalGetter = descriptor.get;
                    Object.defineProperty(Navigator.prototype, prop, {
                        get: function() {
                            const value = originalGetter.apply(this);
                            logAPICall('navigator', prop, value);
                            return value;
                        },
                        configurable: true
                    });
                }
            } catch (e) {
                console.warn(`Could not intercept navigator.${prop}:`, e);
            }
        }
    });

    // ============================================
    // SCREEN PROPERTIES DETECTION
    // ============================================
    const screenProps = [
        'width', 'height', 'availWidth', 'availHeight', 'colorDepth', 'pixelDepth'
    ];

    screenProps.forEach(prop => {
        if (prop in screen) {
            try {
                const descriptor = Object.getOwnPropertyDescriptor(Screen.prototype, prop) ||
                                 Object.getOwnPropertyDescriptor(screen, prop);
                if (descriptor && descriptor.get) {
                    const originalGetter = descriptor.get;
                    Object.defineProperty(Screen.prototype, prop, {
                        get: function() {
                            const value = originalGetter.apply(this);
                            logAPICall('screen', prop, value);
                            return value;
                        },
                        configurable: true
                    });
                }
            } catch (e) {
                console.warn(`Could not intercept screen.${prop}:`, e);
            }
        }
    });

    // ============================================
    // STORAGE (localStorage, sessionStorage) DETECTION
    // ============================================
    ['localStorage', 'sessionStorage'].forEach(storageName => {
        if (window[storageName]) {
            const storage = window[storageName];
            const originalSetItem = storage.setItem;
            const originalGetItem = storage.getItem;

            storage.setItem = function(key, value) {
                logAPICall('storage', `${storageName}.setItem`, { key: key, value: value });
                return originalSetItem.apply(this, arguments);
            };

            storage.getItem = function(key) {
                const value = originalGetItem.apply(this, arguments);
                logAPICall('storage', `${storageName}.getItem`, { key: key, value: value });
                return value;
            };
        }
    });

    // ============================================
    // WEBRTC FINGERPRINTING DETECTION
    // ============================================
    if (typeof RTCPeerConnection !== 'undefined') {
        const originalRTC = RTCPeerConnection;
        window.RTCPeerConnection = function(...args) {
            logAPICall('webrtc', 'RTCPeerConnection', 'constructor called');
            return new originalRTC(...args);
        };
        window.RTCPeerConnection.prototype = originalRTC.prototype;
    }

    if (typeof webkitRTCPeerConnection !== 'undefined') {
        const originalWebkitRTC = webkitRTCPeerConnection;
        window.webkitRTCPeerConnection = function(...args) {
            logAPICall('webrtc', 'webkitRTCPeerConnection', 'constructor called');
            return new originalWebkitRTC(...args);
        };
        window.webkitRTCPeerConnection.prototype = originalWebkitRTC.prototype;
    }

    // ============================================
    // BATTERY API DETECTION
    // ============================================
    if (navigator.getBattery) {
        const originalGetBattery = navigator.getBattery;
        navigator.getBattery = function() {
            logAPICall('battery', 'getBattery', 'called');
            return originalGetBattery.apply(this, arguments);
        };
    }

    // ============================================
    // SENSOR APIs DETECTION (Gyroscope, Accelerometer, etc.)
    // ============================================
    ['Gyroscope', 'Accelerometer', 'LinearAccelerationSensor', 'Magnetometer'].forEach(sensorName => {
        if (window[sensorName]) {
            const OriginalSensor = window[sensorName];
            window[sensorName] = function(...args) {
                logAPICall('sensors', sensorName, 'constructor called');
                return new OriginalSensor(...args);
            };
            window[sensorName].prototype = OriginalSensor.prototype;
        }
    });

    // ============================================
    // PERFORMANCE/TIMING API DETECTION
    // ============================================
    if (performance && performance.timing) {
        const descriptor = Object.getOwnPropertyDescriptor(Performance.prototype, 'timing') ||
                         Object.getOwnPropertyDescriptor(performance, 'timing');
        if (descriptor && descriptor.get) {
            const originalGetter = descriptor.get;
            Object.defineProperty(Performance.prototype, 'timing', {
                get: function() {
                    const value = originalGetter.apply(this);
                    logAPICall('timing', 'performance.timing', 'accessed');
                    return value;
                },
                configurable: true
            });
        }
    }

    // ============================================
    // HARDWARE CONCURRENCY DETECTION
    // ============================================
    if ('hardwareConcurrency' in navigator) {
        try {
            const descriptor = Object.getOwnPropertyDescriptor(Navigator.prototype, 'hardwareConcurrency');
            if (descriptor && descriptor.get) {
                const originalGetter = descriptor.get;
                Object.defineProperty(Navigator.prototype, 'hardwareConcurrency', {
                    get: function() {
                        const value = originalGetter.apply(this);
                        logAPICall('hardware', 'hardwareConcurrency', value);
                        return value;
                    },
                    configurable: true
                });
            }
        } catch (e) {
            console.warn('Could not intercept hardwareConcurrency:', e);
        }
    }

    // ============================================
    // PLUGINS ENUMERATION DETECTION
    // ============================================
    if (navigator.plugins) {
        const originalPlugins = navigator.plugins;
        const pluginsProxy = new Proxy(originalPlugins, {
            get: function(target, prop) {
                logAPICall('plugins', 'navigator.plugins', prop);
                return target[prop];
            }
        });
        
        try {
            Object.defineProperty(navigator, 'plugins', {
                get: function() {
                    logAPICall('plugins', 'navigator.plugins', 'accessed');
                    return pluginsProxy;
                },
                configurable: true
            });
        } catch (e) {
            console.warn('Could not intercept plugins:', e);
        }
    }

    // ============================================
    // EXPORT FUNCTION TO RETRIEVE COLLECTED DATA
    // ============================================
    window.getFingerprintData = function() {
        return {
            data: window.fingerprintData,
            duration: Date.now() - window.detectionStartTime,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            url: window.location.href
        };
    };

    // ============================================
    // CALCULATE STATS
    // ============================================
    window.getFingerprintStats = function() {
        const stats = {};
        let totalCalls = 0;
        
        for (const category in window.fingerprintData) {
            const count = window.fingerprintData[category].length;
            stats[category] = count;
            totalCalls += count;
        }
        
        stats.total = totalCalls;
        stats.duration = Date.now() - window.detectionStartTime;
        
        return stats;
    };

    console.log('Browser Fingerprinting Detection Module loaded successfully');
})();

