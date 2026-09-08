#!/usr/bin/env python3
"""溶氧量估算模块 - Benson & Krause (1984) 国际标准公式"""

import math


def benson_krause_do_saturation(water_temp_c: float, pressure_hpa: float = 1013.25, salinity: float = 0.0) -> float:
    """
    基于 USGS 推荐的经验公式计算淡水饱和溶氧量 (mg/L)

    采用 Weiss (1970) 简化公式，与 Benson & Krause (1984) 数据高度一致。

    Args:
        water_temp_c: 水温(°C)
        pressure_hpa: 大气压(hPa)，默认标准大气压
        salinity: 盐度(‰)，淡水=0

    Returns:
        饱和溶氧量(mg/L)
    """
    T = water_temp_c + 273.15  # 绝对温度(K)
    Ts = math.log((298.15 - water_temp_c) / T)

    # Weiss (1970) / Garcia & Gordon (1992) 系数
    # 输出单位直接为 mL(STP)/L，再换算为 mg/L
    A0 = 2.00907
    A1 = 3.22014
    A2 = 4.05010
    A3 = 4.94457
    A4 = -0.256847
    A5 = 3.88767
    B0 = -0.00624523
    B1 = -0.00737614
    B2 = -0.0103410
    B3 = -0.00817083
    C0 = -0.000000488682

    S = salinity  # 盐度 ‰

    ln_C = (
        A0 + A1 * Ts + A2 * Ts**2 + A3 * Ts**3 + A4 * Ts**4 + A5 * Ts**5
        + S * (B0 + B1 * Ts + B2 * Ts**2 + B3 * Ts**3)
        + C0 * S**2
    )

    # mL(STP)/L → mg/L (乘以 O2 密度 1.42903 mg/mL at STP)
    Cs_mgL = math.exp(ln_C) * 1.42903

    # 气压修正
    P_std = 1013.25
    Cs_corrected = Cs_mgL * (pressure_hpa / P_std)

    return round(Cs_corrected, 2)


def estimate_actual_do(
    water_temp_c: float,
    pressure_hpa: float = 1013.25,
    hour: int = 12,
    cloud_cover_pct: float = 50.0,
    is_deep_water: bool = False,
) -> dict:
    """
    估算实际溶氧量

    Args:
        water_temp_c: 水温(°C)
        pressure_hpa: 大气压(hPa)
        hour: 当前小时(0-23)
        cloud_cover_pct: 云量(%)
        is_deep_water: 是否深水区

    Returns:
        {"saturation": float, "percentage": float, "actual": float, "evaluation": str}
    """
    saturation = benson_krause_do_saturation(water_temp_c, pressure_hpa)

    # 饱和百分比估算
    if is_deep_water:
        pct = 0.60
    elif 4 <= hour <= 6:
        pct = 0.47  # 清晨日出前最低
    elif 7 <= hour <= 9:
        pct = 0.65  # 日出后回升
    elif 10 <= hour <= 14:
        if cloud_cover_pct > 70:
            pct = 0.72  # 阴天午间
        else:
            pct = 0.65  # 晴天午间（温度高抵消光合作用）
    elif 15 <= hour <= 17:
        pct = 0.68  # 午后
    elif 18 <= hour <= 20:
        pct = 0.70  # 傍晚
    else:
        pct = 0.55  # 夜间

    actual = round(saturation * pct, 2)

    # 评价
    if actual >= 7.0:
        evaluation = "充足，鱼类非常活跃"
    elif actual >= 6.0:
        evaluation = "良好，鱼类活跃"
    elif actual >= 5.0:
        evaluation = "中等，鱼类活性一般"
    elif actual >= 4.0:
        evaluation = "偏低，鱼类活性减弱"
    else:
        evaluation = "不足，鱼类可能浮头"

    return {
        "saturation": saturation,
        "percentage": round(pct * 100, 1),
        "actual": actual,
        "evaluation": evaluation,
    }


# 参考表
DO_REFERENCE = {
    0: 14.62, 5: 12.80, 10: 11.33, 15: 10.08,
    18: 9.47, 19: 9.28, 20: 9.09, 22: 8.73,
    24: 8.40, 26: 8.09, 28: 7.81, 30: 7.56,
}


if __name__ == "__main__":
    # 验证: fishweather 惠州实测 溶氧5.6mg/L, 水温24.4°C
    result = estimate_actual_do(24.4, 1008.0, hour=14, cloud_cover_pct=66)
    print(f"水温24.4°C, 气压1008hPa, 14时:")
    print(f"  饱和溶氧: {result['saturation']} mg/L")
    print(f"  饱和百分比: {result['percentage']}%")
    print(f"  估算实际溶氧: {result['actual']} mg/L")
    print(f"  评价: {result['evaluation']}")
    print(f"  fishweather实测: 5.6 mg/L")
