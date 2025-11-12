"""
Script to generate sample HR data
Run this script once to create sample_hr_data.csv
"""
from utils.data_loader import generate_sample_data

if __name__ == "__main__":
    print("Generating sample HR data...")
    df = generate_sample_data()
    print(f"✅ Generated {len(df)} sample records")
    print(f"📁 Saved to: data/sample_hr_data.csv")
    print("\nSample data preview:")
    print(df.head())

