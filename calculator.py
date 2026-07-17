from math import sin, cos, atan2, sqrt, radians, degrees

class OutOfRangeException(Exception):
    pass

# Физические константы мины
INITIAL_SPEED = 14.05  
DRAG = 0.995
GRAVITY = 0.05

def simulate_distance(pitch, target_y, cannon_y):
    """Потиковая симуляция полета снаряда под углом Pitch к горизонту"""
    vh = INITIAL_SPEED * cos(radians(pitch))
    vy = INITIAL_SPEED * sin(radians(pitch))
    
    x = 0.0
    y = float(cannon_y)
    ticks = 0
    hit = False
    
    while ticks < 3000:
        x += vh
        y += vy
        vh *= DRAG
        vy = vy * DRAG - GRAVITY
        ticks += 1
        
        if vy < 0 and y <= target_y:
            hit = True
            break
            
    if not hit:
        return 0.0, ticks
    return x, ticks

def BallisticsToTarget(cannon, target):
    Dx = target[0] - cannon[0]
    Dz = target[2] - cannon[2]
    distance = sqrt(Dx * Dx + Dz * Dz)

    if distance == 0:
        raise OutOfRangeException("Цель находится прямо на координатах миномёта!")

    # Абсолютный Yaw цели в Майнкрафте (0 = Юг, 90 = Запад, 180 = Север, 270 = Восток)
    final_yaw = degrees(atan2(-Dx, Dz)) % 360

    # Проверяем доступность дистанции в пределах от 15 до 85 градусов
    # Сначала ищем решение в навесном секторе (миномётный: 45° - 85°)
    high_arc_found = False
    low = 45.0
    high = 85.0
    pitch = 45.0
    best_ticks = 0

    dist_45, _ = simulate_distance(45.0, target[1], cannon[1])
    dist_85, _ = simulate_distance(85.0, target[1], cannon[1])
    
    min_high_dist = min(dist_45, dist_85)
    max_high_dist = max(dist_45, dist_85)

    if min_high_dist <= distance <= max_high_dist:
        high_arc_found = True
        for _ in range(25):
            mid = (low + high) / 2
            sim_x, ticks = simulate_distance(mid, target[1], cannon[1])
            pitch = mid
            best_ticks = ticks
            if sim_x < distance:
                high = mid  # Недолёт навесом -> уменьшаем угол к 45°
            else:
                low = mid   # Перелёт навесом -> поднимаем ствол к 85°
    
    # Если навесом попасть нельзя, переключаемся на настильный сектор (15° - 45°)
    if not high_arc_found:
        dist_15, _ = simulate_distance(15.0, target[1], cannon[1])
        min_low_dist = min(dist_15, dist_45)
        max_low_dist = max(dist_15, dist_45)
        
        if min_low_dist <= distance <= max_low_dist:
            low = 15.0
            high = 45.0
            for _ in range(25):
                mid = (low + high) / 2
                sim_x, ticks = simulate_distance(mid, target[1], cannon[1])
                pitch = mid
                best_ticks = ticks
                if sim_x < distance:
                    low = mid   # Недолёт -> поднимаем ствол к 45°
                else:
                    high = mid  # Перелёт -> опускаем ствол к 15°
        else:
            raise OutOfRangeException(
                f"Цель недостижима в лимитах 15°-85°! Макс. дальность: {round(dist_45, 1)} бл. "
                f"(Требуется: {round(distance, 1)} бл.)"
            )

    airtimeSeconds = best_ticks / 20
    fuzeTime = int(best_ticks - 5)  # Детонация за 5 тиков до удара

    return (pitch, final_yaw, best_ticks, round(airtimeSeconds, 2), fuzeTime)