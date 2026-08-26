def eos80_density(salinity, temperature, depth_m):
    """간소화된 EOS-80 해수 밀도 산출 (kg/m^3)"""
    s, t, z = float(salinity), float(temperature), float(depth_m)
    if not (0 <= s <= 50 and -5 <= t <= 45): return None
    
    # 1기압 기준 밀도 추정 (약식)
    rho_w = 999.842 + 0.067*t - 0.009*t**2
    rho0 = rho_w + 0.824*s - 0.004*s*t
    
    # 수심(압력)에 따른 압축 보정
    p = z / 10.0 
    k = 19652.2 + 148.4*t + 54.67*s
    
    density = rho0 / (1.0 - p / k)
    return density if 990 <= density <= 1100 else None

def convert_nutrient_unit(value_raw, unit_raw, temp, sal, depth):
    val = float(value_raw)
    
    if unit_raw == 'µmol/L':
        return val, 'Q0'
        
    if unit_raw == 'µmol/kg':
        density = eos80_density(sal, temp, depth)
        if density:
            # 밀도를 곱해 부피 단위로 변환 ( / 1000은 kg_L 변환)
            return val * (density / 1000.0), 'Q0'
            
    return None, 'Q3' # 변환 불가

# ==== 실행 테스트 (더미 데이터) ====
# if __name__ == "__main__":
#     val_kg = 30.5 # umol/kg
#     val_L, qc = convert_nutrient_unit(val_kg, 'µmol/kg', temp=2.0, sal=34.5, depth=100)
#     print(f"변환 전: {val_kg} µmol/kg -> 변환 후: {val_L:.2f} µmol/L (QC: {qc})")