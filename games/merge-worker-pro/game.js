/**
 * 抖音小游戏适配层
 * 用于处理抖音 API 和微信 API 的差异
 */

// 判断运行环境
const isTikTok = typeof tt !== 'undefined';
const isWeChat = typeof wx !== 'undefined';

// 统一 API
const platform = isTikTok ? tt : (isWeChat ? wx : null);

// 导出适配方法
window.platform = platform;
window.isTikTok = isTikTok;
window.isWeChat = isWeChat;

// 分享功能
function shareGame() {
    if (!platform) {
        // 浏览器环境，复制到剪贴板
        const text = `🎮 合成打工人地狱模式\n我打到了第 ${currentLevel + 1} 关！\n来挑战我吧！`;
        navigator.clipboard.writeText(text);
        return;
    }

    platform.shareAppMessage({
        title: '合成打工人 - 地狱模式',
        desc: '超难！你能过几关？',
        imageUrl: 'share.png',
        query: `level=${currentLevel + 1}`,
        success: () => {
            console.log('分享成功');
        },
        fail: (e) => {
            console.log('分享失败', e);
        }
    });
}

// 激励视频广告
let rewardedAd = null;

function initRewardedAd(adUnitId) {
    if (!platform || !platform.createRewardedVideoAd) return null;
    
    rewardedAd = platform.createRewardedVideoAd({
        adUnitId: adUnitId || '你的广告位ID'
    });
    
    rewardedAd.onLoad(() => {
        console.log('激励视频广告加载成功');
    });
    
    rewardedAd.onError((err) => {
        console.log('激励视频广告错误', err);
    });
    
    rewardedAd.onClose((res) => {
        if (res && res.isEnded) {
            // 正常播放结束，发放奖励
            console.log('观看完成，发放奖励');
            if (window.onAdReward) {
                window.onAdReward();
            }
        } else {
            // 播放中途退出，不发放奖励
            console.log('播放未完成');
        }
    });
    
    return rewardedAd;
}

function showRewardedAd(callback) {
    if (!rewardedAd) {
        // 没有广告，模拟成功（测试用）
        setTimeout(callback, 1000);
        return;
    }
    
    window.onAdReward = callback;
    rewardedAd.show().catch(() => {
        // 失败重试
        rewardedAd.load().then(() => rewardedAd.show());
    });
}

// Banner 广告
let bannerAd = null;

function showBannerAd(adUnitId) {
    if (!platform || !platform.createBannerAd) return;
    
    const { windowWidth, windowHeight } = platform.getSystemInfoSync();
    
    bannerAd = platform.createBannerAd({
        adUnitId: adUnitId || '你的Banner广告位ID',
        style: {
            left: 0,
            top: windowHeight - 100,
            width: windowWidth
        }
    });
    
    bannerAd.onResize((size) => {
        bannerAd.style.top = windowHeight - size.height;
        bannerAd.style.left = (windowWidth - size.width) / 2;
    });
    
    bannerAd.show();
}

function hideBannerAd() {
    if (bannerAd) {
        bannerAd.hide();
    }
}

// 插屏广告
let interstitialAd = null;

function initInterstitialAd(adUnitId) {
    if (!platform || !platform.createInterstitialAd) return null;
    
    interstitialAd = platform.createInterstitialAd({
        adUnitId: adUnitId || '你的插屏广告位ID'
    });
    
    interstitialAd.onClose(() => {
        console.log('插屏广告关闭');
    });
    
    interstitialAd.onError((err) => {
        console.log('插屏广告错误', err);
    });
    
    return interstitialAd;
}

function showInterstitialAd() {
    if (!interstitialAd) return;
    interstitialAd.show().catch(() => {
        interstitialAd.load().then(() => interstitialAd.show());
    });
}

// 震动反馈
function vibrate(type = 'short') {
    if (!platform) return;
    
    if (type === 'long') {
        platform.vibrateLong && platform.vibrateLong();
    } else {
        platform.vibrateShort && platform.vibrateShort();
    }
}

// 存储数据
function saveData(key, data) {
    if (!platform) {
        localStorage.setItem(key, JSON.stringify(data));
        return;
    }
    
    platform.setStorageSync(key, JSON.stringify(data));
}

function loadData(key) {
    if (!platform) {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    }
    
    const data = platform.getStorageSync(key);
    return data ? JSON.parse(data) : null;
}

// 导出全局方法
window.shareGame = shareGame;
window.initRewardedAd = initRewardedAd;
window.showRewardedAd = showRewardedAd;
window.showBannerAd = showBannerAd;
window.hideBannerAd = hideBannerAd;
window.initInterstitialAd = initInterstitialAd;
window.showInterstitialAd = showInterstitialAd;
window.vibrate = vibrate;
window.saveData = saveData;
window.loadData = loadData;

console.log('游戏平台适配完成', isTikTok ? '抖音' : (isWeChat ? '微信' : '浏览器'));