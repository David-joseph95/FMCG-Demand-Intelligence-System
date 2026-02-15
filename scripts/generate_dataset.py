"""
================================================================================
ENTERPRISE DEMAND INTELLIGENCE DATA GENERATION ENGINE
================================================================================
Project: Demand Volatility Intelligence System for Nigerian FMCG Operations
Author: David (Supply Chain Intelligence Analyst)
Purpose: Generate 3 years of realistic daily transactional sales data
Dataset: 48 SKUs | 6 Regions | 3 Years (2022-2024) | Daily Granularity
================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

# ============================================================================
# CONFIGURATION PARAMETERS
# ============================================================================

START_DATE = '2022-01-01'
END_DATE = '2024-12-31'
REGIONS = ['Lagos', 'Abuja', 'Port Harcourt', 'Kano', 'Ibadan', 'Enugu']

# ============================================================================
# CHI LIMITED REALISTIC PRODUCT PORTFOLIO (48 SKUs)
# ============================================================================

PRODUCTS = {
    # HOLLANDIA MILK PRODUCTS (12 SKUs)
    'HOL-EVAP-400': {'name': 'Hollandia Evaporated Milk 400g', 'category': 'Milk', 'base_price': 850, 'base_demand': 450},
    'HOL-EVAP-170': {'name': 'Hollandia Evaporated Milk 170g', 'category': 'Milk', 'base_price': 400, 'base_demand': 520},
    'HOL-EVAP-62': {'name': 'Hollandia Evaporated Milk 62g', 'category': 'Milk', 'base_price': 180, 'base_demand': 680},
    'HOL-YOGH-500V': {'name': 'Hollandia Yoghurt Vanilla 500ml', 'category': 'Yoghurt', 'base_price': 600, 'base_demand': 380},
    'HOL-YOGH-500S': {'name': 'Hollandia Yoghurt Strawberry 500ml', 'category': 'Yoghurt', 'base_price': 600, 'base_demand': 390},
    'HOL-YOGH-100V': {'name': 'Hollandia Yoghurt Vanilla 100ml', 'category': 'Yoghurt', 'base_price': 150, 'base_demand': 550},
    'HOL-YOGH-100S': {'name': 'Hollandia Yoghurt Strawberry 100ml', 'category': 'Yoghurt', 'base_price': 150, 'base_demand': 560},
    'HOL-SMART-200': {'name': 'Hollandia Smartee Milk Drink 200ml', 'category': 'Milk Drink', 'base_price': 200, 'base_demand': 620},
    'HOL-SMART-500': {'name': 'Hollandia Smartee Milk Drink 500ml', 'category': 'Milk Drink', 'base_price': 450, 'base_demand': 420},
    'HOL-UHT-1L': {'name': 'Hollandia UHT Milk 1L', 'category': 'Milk', 'base_price': 1200, 'base_demand': 320},
    'HOL-UHT-500': {'name': 'Hollandia UHT Milk 500ml', 'category': 'Milk', 'base_price': 650, 'base_demand': 410},
    'HOL-CHOC-200': {'name': 'Hollandia Chocolate Milk 200ml', 'category': 'Milk Drink', 'base_price': 250, 'base_demand': 480},
    
    # CHIVITA JUICE PRODUCTS (18 SKUs)
    'CHV-100-ORG-1L': {'name': 'Chivita 100% Orange Juice 1L', 'category': 'Juice', 'base_price': 1500, 'base_demand': 350},
    'CHV-100-ORG-500': {'name': 'Chivita 100% Orange Juice 500ml', 'category': 'Juice', 'base_price': 800, 'base_demand': 420},
    'CHV-100-ORG-315': {'name': 'Chivita 100% Orange Juice 315ml', 'category': 'Juice', 'base_price': 550, 'base_demand': 490},
    'CHV-100-APP-1L': {'name': 'Chivita 100% Apple Juice 1L', 'category': 'Juice', 'base_price': 1600, 'base_demand': 280},
    'CHV-100-APP-500': {'name': 'Chivita 100% Apple Juice 500ml', 'category': 'Juice', 'base_price': 850, 'base_demand': 340},
    'CHV-100-PIN-1L': {'name': 'Chivita 100% Pineapple Juice 1L', 'category': 'Juice', 'base_price': 1550, 'base_demand': 300},
    'CHV-100-PIN-500': {'name': 'Chivita 100% Pineapple Juice 500ml', 'category': 'Juice', 'base_price': 820, 'base_demand': 370},
    'CHV-EXO-TROP-1L': {'name': 'Chi Exotic Tropical Blend 1L', 'category': 'Juice', 'base_price': 1400, 'base_demand': 360},
    'CHV-EXO-TROP-500': {'name': 'Chi Exotic Tropical Blend 500ml', 'category': 'Juice', 'base_price': 750, 'base_demand': 430},
    'CHV-EXO-TROP-315': {'name': 'Chi Exotic Tropical Blend 315ml', 'category': 'Juice', 'base_price': 520, 'base_demand': 500},
    'CHV-ACT-STRA-315': {'name': 'Chivita Active Yoghurt Strawberry 315ml', 'category': 'Yoghurt', 'base_price': 500, 'base_demand': 440},
    'CHV-ACT-STRA-500': {'name': 'Chivita Active Yoghurt Strawberry 500ml', 'category': 'Yoghurt', 'base_price': 750, 'base_demand': 380},
    'CHV-ACT-VAN-315': {'name': 'Chivita Active Yoghurt Vanilla 315ml', 'category': 'Yoghurt', 'base_price': 500, 'base_demand': 430},
    'CHV-ACT-VAN-500': {'name': 'Chivita Active Yoghurt Vanilla 500ml', 'category': 'Yoghurt', 'base_price': 750, 'base_demand': 370},
    'CHV-ACT-MIX-315': {'name': 'Chivita Active Yoghurt Mixed Fruit 315ml', 'category': 'Yoghurt', 'base_price': 500, 'base_demand': 410},
    'CHV-ICE-ORG-200': {'name': 'Chivita Ice Tea Orange 200ml', 'category': 'Ice Tea', 'base_price': 300, 'base_demand': 520},
    'CHV-ICE-LEM-200': {'name': 'Chivita Ice Tea Lemon 200ml', 'category': 'Ice Tea', 'base_price': 300, 'base_demand': 530},
    'CHV-ICE-PEA-200': {'name': 'Chivita Ice Tea Peach 200ml', 'category': 'Ice Tea', 'base_price': 300, 'base_demand': 510},
    
    # CHI SNACKS & BEVERAGES (10 SKUs)
    'CHI-NUT-CHO-50': {'name': 'Chi Nutri Chocolate 50g', 'category': 'Snacks', 'base_price': 350, 'base_demand': 480},
    'CHI-NUT-VAN-50': {'name': 'Chi Nutri Vanilla 50g', 'category': 'Snacks', 'base_price': 350, 'base_demand': 460},
    'CHI-NUT-STR-50': {'name': 'Chi Nutri Strawberry 50g', 'category': 'Snacks', 'base_price': 350, 'base_demand': 470},
    'CHI-CEREAL-CHO-35': {'name': 'Chi Cereal Drink Chocolate 35g', 'category': 'Cereal Drink', 'base_price': 250, 'base_demand': 540},
    'CHI-CEREAL-VAN-35': {'name': 'Chi Cereal Drink Vanilla 35g', 'category': 'Cereal Drink', 'base_price': 250, 'base_demand': 550},
    'CHI-ENERGY-ORG-330': {'name': 'Chi Energy Drink Orange 330ml', 'category': 'Energy Drink', 'base_price': 450, 'base_demand': 400},
    'CHI-ENERGY-BER-330': {'name': 'Chi Energy Drink Berry 330ml', 'category': 'Energy Drink', 'base_price': 450, 'base_demand': 390},
    'CHI-WATER-750': {'name': 'Chi Table Water 750ml', 'category': 'Water', 'base_price': 150, 'base_demand': 700},
    'CHI-WATER-1500': {'name': 'Chi Table Water 1.5L', 'category': 'Water', 'base_price': 250, 'base_demand': 650},
    'CHI-WATER-500': {'name': 'Chi Table Water 500ml', 'category': 'Water', 'base_price': 100, 'base_demand': 750},
    
    # CHI INNOVATIONS (8 SKUs)
    'CHI-SMOOTH-MAN-350': {'name': 'Chi Smoothie Mango 350ml', 'category': 'Smoothie', 'base_price': 650, 'base_demand': 320},
    'CHI-SMOOTH-BER-350': {'name': 'Chi Smoothie Mixed Berry 350ml', 'category': 'Smoothie', 'base_price': 650, 'base_demand': 310},
    'CHI-SMOOTH-STRA-350': {'name': 'Chi Smoothie Strawberry 350ml', 'category': 'Smoothie', 'base_price': 650, 'base_demand': 330},
    'CHI-PROTEIN-CHO-330': {'name': 'Chi Protein Shake Chocolate 330ml', 'category': 'Protein Shake', 'base_price': 800, 'base_demand': 250},
    'CHI-PROTEIN-VAN-330': {'name': 'Chi Protein Shake Vanilla 330ml', 'category': 'Protein Shake', 'base_price': 800, 'base_demand': 240},
    'CHI-ALMOND-1L': {'name': 'Chi Almond Milk 1L', 'category': 'Plant Milk', 'base_price': 1800, 'base_demand': 180},
    'CHI-SOY-1L': {'name': 'Chi Soy Milk 1L', 'category': 'Plant Milk', 'base_price': 1600, 'base_demand': 200},
    'CHI-COCONUT-1L': {'name': 'Chi Coconut Milk 1L', 'category': 'Plant Milk', 'base_price': 1700, 'base_demand': 190},
}

# ============================================================================
# NIGERIAN HOLIDAY CALENDAR (EXACT DATES 2022-2024)
# ============================================================================

HOLIDAYS = {
    # 2022
    '2022-01-01': 'New Year',
    '2022-04-02': 'Ramadan Start',
    '2022-05-01': 'Ramadan End',
    '2022-05-02': 'Eid al-Fitr Day 1',
    '2022-05-03': 'Eid al-Fitr Day 2',
    '2022-05-04': 'Eid al-Fitr Day 3',
    '2022-05-27': 'Children\'s Day',
    '2022-07-09': 'Eid al-Adha Day 1',
    '2022-07-10': 'Eid al-Adha Day 2',
    '2022-07-11': 'Eid al-Adha Day 3',
    '2022-09-05': 'Back to School Start',
    '2022-09-30': 'Back to School End',
    '2022-10-01': 'Independence Day',
    '2022-12-20': 'Christmas Season Start',
    '2022-12-25': 'Christmas Day',
    '2022-12-26': 'Boxing Day',
    '2022-12-31': 'New Year Eve',
    
    # 2023
    '2023-01-01': 'New Year',
    '2023-03-23': 'Ramadan Start',
    '2023-04-21': 'Ramadan End',
    '2023-04-22': 'Eid al-Fitr Day 1',
    '2023-04-23': 'Eid al-Fitr Day 2',
    '2023-04-24': 'Eid al-Fitr Day 3',
    '2023-05-27': 'Children\'s Day',
    '2023-06-28': 'Eid al-Adha Day 1',
    '2023-06-29': 'Eid al-Adha Day 2',
    '2023-06-30': 'Eid al-Adha Day 3',
    '2023-09-04': 'Back to School Start',
    '2023-09-29': 'Back to School End',
    '2023-10-01': 'Independence Day',
    '2023-12-20': 'Christmas Season Start',
    '2023-12-25': 'Christmas Day',
    '2023-12-26': 'Boxing Day',
    '2023-12-31': 'New Year Eve',
    
    # 2024
    '2024-01-01': 'New Year',
    '2024-03-11': 'Ramadan Start',
    '2024-04-09': 'Ramadan End',
    '2024-04-10': 'Eid al-Fitr Day 1',
    '2024-04-11': 'Eid al-Fitr Day 2',
    '2024-04-12': 'Eid al-Fitr Day 3',
    '2024-05-27': 'Children\'s Day',
    '2024-06-16': 'Eid al-Adha Day 1',
    '2024-06-17': 'Eid al-Adha Day 2',
    '2024-06-18': 'Eid al-Adha Day 3',
    '2024-09-02': 'Back to School Start',
    '2024-09-27': 'Back to School End',
    '2024-10-01': 'Independence Day',
    '2024-12-20': 'Christmas Season Start',
    '2024-12-25': 'Christmas Day',
    '2024-12-26': 'Boxing Day',
    '2024-12-31': 'New Year Eve',
}

# ============================================================================
# REGIONAL CHARACTERISTICS
# ============================================================================

REGIONAL_MULTIPLIERS = {
    'Lagos': {'demand': 1.45, 'promotion_response': 1.35, 'volatility': 1.20},
    'Abuja': {'demand': 1.15, 'promotion_response': 1.20, 'volatility': 1.10},
    'Port Harcourt': {'demand': 0.95, 'promotion_response': 1.15, 'volatility': 1.15},
    'Kano': {'demand': 1.05, 'promotion_response': 0.95, 'volatility': 1.25},
    'Ibadan': {'demand': 0.85, 'promotion_response': 1.10, 'volatility': 1.05},
    'Enugu': {'demand': 0.75, 'promotion_response': 1.05, 'volatility': 1.00},
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_holiday_effect(date_str, holiday_name):
    """Calculate demand multiplier based on holiday type and timing"""
    
    # Major holidays with strong pre-purchase patterns
    if 'Christmas' in holiday_name:
        return np.random.uniform(2.2, 2.8)
    elif 'Eid al-Fitr' in holiday_name:
        return np.random.uniform(1.8, 2.4)
    elif 'Eid al-Adha' in holiday_name:
        return np.random.uniform(1.6, 2.2)
    elif 'New Year' in holiday_name:
        return np.random.uniform(1.5, 2.0)
    elif 'Back to School' in holiday_name:
        return np.random.uniform(1.3, 1.7)
    elif 'Children\'s Day' in holiday_name:
        return np.random.uniform(1.2, 1.5)
    elif 'Independence Day' in holiday_name:
        return np.random.uniform(1.1, 1.4)
    elif 'Ramadan' in holiday_name:
        return np.random.uniform(0.7, 0.9)  # Lower demand during fasting
    else:
        return 1.0

def get_pre_holiday_effect(days_to_holiday, holiday_type):
    """Calculate pre-holiday demand surge"""
    if days_to_holiday > 14:
        return 1.0
    elif days_to_holiday <= 14 and days_to_holiday > 7:
        return 1.0 + (0.15 * (14 - days_to_holiday) / 7)
    elif days_to_holiday <= 7 and days_to_holiday > 0:
        if 'Christmas' in holiday_type or 'Eid' in holiday_type:
            return 1.15 + (0.35 * (7 - days_to_holiday) / 7)
        else:
            return 1.10 + (0.20 * (7 - days_to_holiday) / 7)
    else:
        return 1.0

def get_post_holiday_effect(days_after_holiday):
    """Calculate post-holiday demand slump"""
    if days_after_holiday > 7:
        return 1.0
    elif days_after_holiday <= 7 and days_after_holiday > 0:
        return 0.75 + (0.25 * days_after_holiday / 7)
    else:
        return 1.0

def get_day_of_week_effect(day_name):
    """Weekday vs weekend patterns"""
    weekend_boost = {'Saturday': 1.25, 'Sunday': 1.15}
    weekday_normal = {'Monday': 0.95, 'Tuesday': 1.00, 'Wednesday': 1.05, 
                      'Thursday': 1.08, 'Friday': 1.18}
    
    if day_name in weekend_boost:
        return weekend_boost[day_name]
    else:
        return weekday_normal.get(day_name, 1.0)

def generate_promotion_calendar(date_range):
    """Generate realistic promotion schedule"""
    promotions = {}
    
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        month = date.month
        day = date.day
        
        # Strategic promotion windows
        promo_prob = 0.05  # Base 5% chance
        
        # Increase during competitive periods
        if month in [3, 4, 6, 7, 9, 12]:  # Before major holidays
            promo_prob = 0.15
        
        if np.random.random() < promo_prob:
            promo_type = np.random.choice(
                ['Discount', 'BOGO', 'Bundle', 'Volume Discount'],
                p=[0.50, 0.25, 0.15, 0.10]
            )
            
            if promo_type == 'Discount':
                discount = np.random.choice([5, 10, 15, 20, 25], p=[0.15, 0.35, 0.30, 0.15, 0.05])
            elif promo_type == 'BOGO':
                discount = 50  # Effective discount
            elif promo_type == 'Bundle':
                discount = np.random.choice([10, 15, 20], p=[0.40, 0.40, 0.20])
            else:
                discount = np.random.choice([10, 15, 20], p=[0.50, 0.30, 0.20])
            
            promotions[date_str] = {'type': promo_type, 'discount': discount}
        else:
            promotions[date_str] = {'type': 'None', 'discount': 0}
    
    return promotions

def calculate_days_to_nearest_holiday(current_date, holiday_dict):
    """Calculate days to nearest upcoming holiday"""
    current_date_str = current_date.strftime('%Y-%m-%d')
    
    # Find nearest upcoming holiday
    min_days = 999
    nearest_holiday = None
    
    for holiday_date_str, holiday_name in holiday_dict.items():
        holiday_date = datetime.strptime(holiday_date_str, '%Y-%m-%d')
        days_diff = (holiday_date - current_date).days
        
        if -7 <= days_diff <= 14:  # Within window
            if abs(days_diff) < abs(min_days):
                min_days = days_diff
                nearest_holiday = holiday_name
    
    return min_days if nearest_holiday else None, nearest_holiday

# ============================================================================
# MAIN DATA GENERATION FUNCTION
# ============================================================================

def generate_enterprise_dataset():
    """Generate complete 3-year daily transactional dataset"""
    
    print("="*80)
    print("ENTERPRISE DATA GENERATION ENGINE - INITIALIZING")
    print("="*80)
    
    # Generate date range
    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    print(f"✓ Date Range: {START_DATE} to {END_DATE} ({len(date_range)} days)")
    
    # Generate promotion calendar
    promotion_calendar = generate_promotion_calendar(date_range)
    print(f"✓ Promotion Calendar Generated")
    
    # Initialize data container
    records = []
    order_id_counter = 100000
    
    print(f"✓ Generating transactions for {len(PRODUCTS)} SKUs across {len(REGIONS)} regions...")
    print(f"✓ Target: ~{len(date_range) * len(PRODUCTS) * len(REGIONS) * 3:,} transactions")
    print("\nGenerating data...")
    
    # Generate transactions
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        day_name = date.strftime('%A')
        month = date.month
        year = date.year
        week_of_year = date.isocalendar()[1]
        
        # Holiday information
        is_holiday = date_str in HOLIDAYS
        holiday_name = HOLIDAYS.get(date_str, 'None')
        
        # Calculate days to/from holidays
        days_to_holiday, nearest_holiday = calculate_days_to_nearest_holiday(date, HOLIDAYS)
        
        # Promotion information
        promotion_info = promotion_calendar[date_str]
        is_promoted = promotion_info['type'] != 'None'
        
        # Day of week effect
        dow_effect = get_day_of_week_effect(day_name)
        
        # Generate transactions for each SKU in each region
        for sku_code, sku_info in PRODUCTS.items():
            for region in REGIONS:
                
                # Number of orders for this SKU-Region-Day (2-5 orders typical)
                num_orders = np.random.randint(2, 6)
                
                for order_num in range(num_orders):
                    order_id_counter += 1
                    
                    # Base demand with realistic noise
                    base_demand = sku_info['base_demand']
                    regional_multiplier = REGIONAL_MULTIPLIERS[region]['demand']
                    
                    # Apply all demand factors
                    demand = base_demand * regional_multiplier * dow_effect
                    
                    # Holiday effects
                    if is_holiday:
                        holiday_effect = get_holiday_effect(date_str, holiday_name)
                        demand *= holiday_effect
                    
                    # Pre/post holiday effects
                    if days_to_holiday is not None:
                        if days_to_holiday > 0:  # Before holiday
                            pre_effect = get_pre_holiday_effect(days_to_holiday, nearest_holiday)
                            demand *= pre_effect
                        elif days_to_holiday < 0:  # After holiday
                            post_effect = get_post_holiday_effect(abs(days_to_holiday))
                            demand *= post_effect
                    
                    # Promotion effects
                    if is_promoted:
                        promo_response = REGIONAL_MULTIPLIERS[region]['promotion_response']
                        discount_pct = promotion_info['discount']
                        
                        # Promotion lift (non-linear with discount depth)
                        if promotion_info['type'] == 'BOGO':
                            promo_lift = 1.8 + np.random.uniform(0, 0.4)
                        elif promotion_info['type'] == 'Bundle':
                            promo_lift = 1.5 + np.random.uniform(0, 0.3)
                        else:
                            promo_lift = 1.0 + (discount_pct / 100) * 2.5
                        
                        demand *= promo_lift * promo_response
                    
                    # Seasonal patterns (annual cycle)
                    seasonal_factor = 1.0 + 0.15 * np.sin(2 * np.pi * month / 12)
                    demand *= seasonal_factor
                    
                    # Add realistic noise (volatility varies by region)
                    volatility = REGIONAL_MULTIPLIERS[region]['volatility']
                    noise = np.random.normal(1.0, 0.12 * volatility)
                    demand *= noise
                    
                    # Final units sold (rounded to integer)
                    units_sold = max(1, int(np.round(demand / num_orders)))
                    
                    # Pricing logic
                    base_price = sku_info['base_price']
                    
                    # Apply promotion discount
                    if is_promoted:
                        unit_price = base_price * (1 - promotion_info['discount'] / 100)
                    else:
                        # Minor price variation (±3%)
                        unit_price = base_price * np.random.uniform(0.97, 1.03)
                    
                    # Calculate revenue
                    revenue = units_sold * unit_price
                    
                    # Inventory simulation
                    # Base inventory = 3x base demand
                    base_inventory = sku_info['base_demand'] * 3
                    inventory_variation = np.random.normal(1.0, 0.15)
                    inventory_eod = int(base_inventory * regional_multiplier * inventory_variation)
                    
                    # Stockout flag (if demand exceeded inventory)
                    stockout_flag = 1 if units_sold >= inventory_eod else 0
                    
                    # Lead time (realistic range for FMCG)
                    lead_time_days = np.random.choice([2, 3, 4, 5, 7], p=[0.15, 0.30, 0.35, 0.15, 0.05])
                    
                    # Customer segment
                    customer_segment = np.random.choice(
                        ['Retail', 'Wholesale', 'Distributor', 'Online'],
                        p=[0.50, 0.25, 0.20, 0.05]
                    )
                    
                    # Fulfillment rate (realistic operational metric)
                    fulfillment_rate = np.random.uniform(0.92, 1.00) if stockout_flag == 0 else np.random.uniform(0.60, 0.85)
                    
                    # Build record
                    record = {
                        'order_id': f'ORD-{order_id_counter:08d}',
                        'order_date': date_str,
                        'year': year,
                        'month': month,
                        'week_of_year': week_of_year,
                        'day_of_week': day_name,
                        'day_of_month': date.day,
                        'quarter': (month - 1) // 3 + 1,
                        
                        'sku_code': sku_code,
                        'product_name': sku_info['name'],
                        'product_category': sku_info['category'],
                        
                        'region': region,
                        'customer_segment': customer_segment,
                        
                        'units_sold': units_sold,
                        'unit_price': round(unit_price, 2),
                        'revenue': round(revenue, 2),
                        
                        'is_promoted': 1 if is_promoted else 0,
                        'promotion_type': promotion_info['type'],
                        'discount_pct': promotion_info['discount'],
                        
                        'is_holiday': 1 if is_holiday else 0,
                        'holiday_name': holiday_name,
                        'days_to_holiday': days_to_holiday if days_to_holiday is not None else 999,
                        'nearest_holiday': nearest_holiday if nearest_holiday else 'None',
                        
                        'inventory_eod': inventory_eod,
                        'stockout_flag': stockout_flag,
                        'lead_time_days': lead_time_days,
                        'fulfillment_rate': round(fulfillment_rate, 4),
                        
                        'is_weekend': 1 if day_name in ['Saturday', 'Sunday'] else 0,
                        'is_month_start': 1 if date.day <= 5 else 0,
                        'is_month_end': 1 if date.day >= 25 else 0,
                    }
                    
                    records.append(record)
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    print(f"\n✓ Data generation complete!")
    print(f"✓ Total records: {len(df):,}")
    print(f"✓ Date range: {df['order_date'].min()} to {df['order_date'].max()}")
    print(f"✓ Total SKUs: {df['sku_code'].nunique()}")
    print(f"✓ Total regions: {df['region'].nunique()}")
    print(f"✓ Total revenue: ₦{df['revenue'].sum():,.2f}")
    
    return df

# ============================================================================
# EXECUTION & EXPORT
# ============================================================================

if __name__ == "__main__":
    
    # Generate dataset
    df_sales = generate_enterprise_dataset()
    
    # Data quality checks
    print("\n" + "="*80)
    print("DATA QUALITY VALIDATION")
    print("="*80)
    print(f"✓ No missing values: {df_sales.isnull().sum().sum() == 0}")
    print(f"✓ Unique orders: {df_sales['order_id'].nunique():,}")
    print(f"✓ Date coverage: {df_sales['order_date'].nunique()} days")
    
    # Summary statistics
    print("\n" + "="*80)
    print("DATASET SUMMARY STATISTICS")
    print("="*80)
    print(f"\nRevenue Statistics:")
    print(f"  Total Revenue: ₦{df_sales['revenue'].sum():,.2f}")
    print(f"  Average Daily Revenue: ₦{df_sales.groupby('order_date')['revenue'].sum().mean():,.2f}")
    print(f"  Revenue Std Dev: ₦{df_sales.groupby('order_date')['revenue'].sum().std():,.2f}")
    
    print(f"\nUnits Sold Statistics:")
    print(f"  Total Units: {df_sales['units_sold'].sum():,}")
    print(f"  Average Order Size: {df_sales['units_sold'].mean():.1f} units")
    print(f"  Max Order Size: {df_sales['units_sold'].max()} units")
    
    print(f"\nPromotion Statistics:")
    print(f"  Promoted Orders: {(df_sales['is_promoted'].sum() / len(df_sales) * 100):.1f}%")
    print(f"  Average Discount: {df_sales[df_sales['is_promoted']==1]['discount_pct'].mean():.1f}%")
    
    print(f"\nHoliday Statistics:")
    print(f"  Holiday Orders: {(df_sales['is_holiday'].sum() / len(df_sales) * 100):.1f}%")
    print(f"  Stockout Rate: {(df_sales['stockout_flag'].sum() / len(df_sales) * 100):.1f}%")
    
    # Regional breakdown
    print(f"\nRevenue by Region:")
    regional_revenue = df_sales.groupby('region')['revenue'].sum().sort_values(ascending=False)
    for region, revenue in regional_revenue.items():
        print(f"  {region}: ₦{revenue:,.2f} ({revenue/df_sales['revenue'].sum()*100:.1f}%)")
    
    # Category breakdown
    print(f"\nRevenue by Category:")
    category_revenue = df_sales.groupby('product_category')['revenue'].sum().sort_values(ascending=False)
    for category, revenue in category_revenue.items():
        print(f"  {category}: ₦{revenue:,.2f} ({revenue/df_sales['revenue'].sum()*100:.1f}%)")
    
    # Export to CSV
    output_file = 'chi_limited_sales_data_2022_2024.csv'
    df_sales.to_csv(output_file, index=False)
    print(f"\n✓ Dataset exported to: {output_file}")
    print(f"✓ File size: {df_sales.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print("\n" + "="*80)
    print("DATA GENERATION COMPLETE - READY FOR ANALYSIS")
    print("="*80)