import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体和图表样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
sns.set_palette("husl")

# ==================== 第一部分：生成20个样本的糖尿病数据集 ====================

print("="*60)
print("生成20个样本的糖尿病数据集")
print("="*60)

np.random.seed(42)  # 设置随机种子以确保可重复性

# 生成20个样本
n_samples = 20

# 生成基础数据
age = np.random.normal(55, 12, n_samples).astype(int)  # 年龄，均值为55，标准差为12
bmi = np.random.normal(28, 4, n_samples)  # BMI，均值为28，标准差为4

# 添加相关性：年龄和BMI对血糖和血压的影响
# 血糖 = 基础值 + BMI影响 + 年龄影响 + 随机噪声
base_glucose = 90  # 基础血糖值
glucose = base_glucose + (bmi - 25) * 3 + (age - 50) * 0.5 + np.random.normal(0, 10, n_samples)

# 血压 = 基础值 + BMI影响 + 年龄影响 + 随机噪声
base_bp = 70  # 基础血压值
bp = base_bp + (bmi - 25) * 1.5 + (age - 50) * 0.3 + np.random.normal(0, 5, n_samples)

# 生成是否患病的标签（基于逻辑回归概率）
# 患病概率 = sigmoid(0.05*血糖 + 0.1*BMI + 0.02*年龄 - 10)
z = 0.05 * glucose + 0.1 * bmi + 0.02 * age - 10
prob = 1 / (1 + np.exp(-z))  # sigmoid函数

# 添加一些随机性，并生成最终标签
diabetes_prob = np.clip(prob, 0.1, 0.9)  # 限制概率在0.1到0.9之间
has_diabetes = np.random.binomial(1, diabetes_prob)  # 根据概率生成二元标签

# 确保至少有3个患病和3个非患病样本（为了可视化效果）
if sum(has_diabetes) < 3:
    # 找出患病概率最高的3个样本，设为患病
    top_indices = np.argsort(diabetes_prob)[-3:]
    has_diabetes[top_indices] = 1
    
if sum(has_diabetes) > n_samples - 3:
    # 找出患病概率最低的3个样本，设为非患病
    bottom_indices = np.argsort(diabetes_prob)[:3]
    has_diabetes[bottom_indices] = 0

# 创建数据字典
data_dict = {
    '患者ID': [f'P{str(i+1).zfill(3)}' for i in range(n_samples)],
    '年龄': age,
    'BMI': np.round(bmi, 1),
    '血糖': np.round(np.clip(glucose, 70, 250), 0),  # 限制在70-250范围内
    '血压': np.round(np.clip(bp, 60, 120), 0),  # 限制在60-120范围内
    '是否患病': has_diabetes.astype(int),
    '患病概率(%)': np.round(diabetes_prob * 100, 1)
}

# 转换为DataFrame
df = pd.DataFrame(data_dict)

# 添加一些额外的特征（为了丰富数据集）
# 根据年龄分组
def age_group(age_val):
    if age_val < 30:
        return '20-29'
    elif age_val < 40:
        return '30-39'
    elif age_val < 50:
        return '40-49'
    elif age_val < 60:
        return '50-59'
    elif age_val < 70:
        return '60-69'
    else:
        return '70+'

df['年龄组'] = df['年龄'].apply(age_group)

# 根据BMI分类
def bmi_category(bmi_val):
    if bmi_val < 18.5:
        return '偏瘦'
    elif bmi_val < 24:
        return '正常'
    elif bmi_val < 28:
        return '偏胖'
    else:
        return '肥胖'

df['BMI分类'] = df['BMI'].apply(bmi_category)

# 根据血糖水平分类
def glucose_category(glucose_val):
    if glucose_val < 100:
        return '正常'
    elif glucose_val < 126:
        return '糖尿病前期'
    else:
        return '糖尿病'

df['血糖分类'] = df['血糖'].apply(glucose_category)

# 显示生成的数据
print("生成的糖尿病数据集（20个样本）：")
print("="*60)
print(df.to_string(index=False))

# 显示基本统计信息
print("\n基本统计信息：")
print("="*60)
print(f"总样本数: {len(df)}")
print(f"患病人数: {sum(df['是否患病'])}")
print(f"患病率: {sum(df['是否患病'])/len(df)*100:.1f}%")
print(f"平均年龄: {df['年龄'].mean():.1f}岁")
print(f"平均BMI: {df['BMI'].mean():.1f}")
print(f"平均血糖: {df['血糖'].mean():.1f} mg/dL")
print(f"平均血压: {df['血压'].mean():.1f} mmHg")

# 保存为Excel文件
excel_filename = '糖尿病数据集_20样本.xlsx'
df.to_excel(excel_filename, index=False)
print(f"\n数据集已保存为: {excel_filename}")

# ==================== 第二部分：可视化分析 ====================

print("\n" + "="*60)
print("开始可视化分析")
print("="*60)

# 1. 绘制血糖与BMI的散点图，颜色区分是否患病
plt.figure(figsize=(12, 8))

# 创建散点图，按是否患病着色
colors = ['blue', 'red']  # 0=健康(蓝色), 1=患病(红色)
color_list = [colors[val] for val in df['是否患病']]

scatter = plt.scatter(
    df['BMI'], 
    df['血糖'], 
    c=color_list, 
    alpha=0.7, 
    s=150,
    edgecolors='w',
    linewidth=1.5
)

# 为每个点添加患者ID标签
for i, row in df.iterrows():
    plt.annotate(row['患者ID'], 
                (row['BMI'], row['血糖']),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=9,
                alpha=0.7)

# 添加回归线
z = np.polyfit(df['BMI'], df['血糖'], 1)
p = np.poly1d(z)
plt.plot(df['BMI'], p(df['BMI']), "k--", alpha=0.8, linewidth=2, label='趋势线')

# 添加分类边界
plt.axhline(y=126, color='green', linestyle='--', alpha=0.5, linewidth=2, label='糖尿病诊断阈值(126)')
plt.axvline(x=28, color='orange', linestyle='--', alpha=0.5, linewidth=2, label='肥胖阈值(BMI=28)')

# 设置图表属性
plt.xlabel('BMI (体重指数)', fontsize=14, fontweight='bold')
plt.ylabel('血糖 (mg/dL)', fontsize=14, fontweight='bold')
plt.title('血糖与BMI的关系散点图（20个样本）', fontsize=16, fontweight='bold')

# 添加图例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='blue', alpha=0.7, label='健康 (是否患病=0)'),
    Patch(facecolor='red', alpha=0.7, label='患病 (是否患病=1)'),
    plt.Line2D([0], [0], color='k', linestyle='--', label='趋势线'),
    plt.Line2D([0], [0], color='green', linestyle='--', label='糖尿病诊断阈值'),
    plt.Line2D([0], [0], color='orange', linestyle='--', label='肥胖阈值')
]
plt.legend(handles=legend_elements, loc='upper left')

# 添加统计信息
correlation, p_value = stats.pearsonr(df['BMI'], df['血糖'])
plt.text(0.02, 0.98, f'相关系数: {correlation:.3f}\nP值: {p_value:.4f}\n样本数: {n_samples}', 
         transform=plt.gca().transAxes, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('血糖_BMI_散点图_20样本.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. 绘制年龄与患病率的箱线图，分组展示
plt.figure(figsize=(14, 6))

# 创建子图
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 子图1: 按患病状态分组的年龄箱线图
sns.boxplot(x='是否患病', y='年龄', data=df, ax=axes[0], palette='Set2')
sns.swarmplot(x='是否患病', y='年龄', data=df, ax=axes[0], color='black', alpha=0.7, size=8)

axes[0].set_title('不同患病状态的年龄分布', fontsize=14, fontweight='bold')
axes[0].set_xlabel('患病状态', fontweight='bold')
axes[0].set_ylabel('年龄', fontweight='bold')
axes[0].set_xticklabels(['健康', '患病'])

# 添加统计信息
for i, group in enumerate([0, 1]):
    age_data = df[df['是否患病'] == group]['年龄']
    if len(age_data) > 0:
        axes[0].text(i, df['年龄'].max() + 2, 
                    f'n={len(age_data)}\n中位数={age_data.median():.0f}岁', 
                    ha='center', va='bottom', fontweight='bold')

# 子图2: 按年龄分组统计患病率
age_group_counts = df.groupby('年龄组').agg({
    '是否患病': ['count', 'sum'],
    '患者ID': lambda x: ', '.join(x)
}).round(2)

age_group_counts.columns = ['总人数', '患病人数', '患者列表']
age_group_counts['患病率(%)'] = (age_group_counts['患病人数'] / age_group_counts['总人数'] * 100).round(1)
age_group_counts = age_group_counts.reset_index()

# 绘制条形图
bars = axes[1].bar(age_group_counts['年龄组'], age_group_counts['患病率(%)'], 
                   color=sns.color_palette('Blues', len(age_group_counts)))
axes[1].set_title('不同年龄组的糖尿病患病率', fontsize=14, fontweight='bold')
axes[1].set_xlabel('年龄分组', fontweight='bold')
axes[1].set_ylabel('患病率 (%)', fontweight='bold')

# 在每个条形上添加数值
for bar, total, sick, rate in zip(bars, age_group_counts['总人数'], 
                                  age_group_counts['患病人数'], age_group_counts['患病率(%)']):
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{rate}%\n({sick}/{total})', ha='center', va='bottom', 
                fontsize=10, fontweight='bold')

# 添加趋势线（如果有多于2个年龄组）
if len(age_group_counts) > 2:
    x_numeric = np.arange(len(age_group_counts))
    z_trend = np.polyfit(x_numeric, age_group_counts['患病率(%)'], 1)
    p_trend = np.poly1d(z_trend)
    axes[1].plot(x_numeric, p_trend(x_numeric), 'r--', alpha=0.7, linewidth=2, label='趋势线')
    axes[1].legend()

plt.tight_layout()
plt.savefig('年龄_患病率_分析_20样本.png', dpi=300, bbox_inches='tight')
plt.show()

# 3. 绘制关键生理指标的热力图，展示相关性
print("\n" + "="*60)
print("关键生理指标相关性分析")
print("="*60)

# 选择关键指标
key_metrics = ['血糖', '血压', 'BMI', '年龄']
if all(col in df.columns for col in key_metrics):
    metrics_df = df[key_metrics]
    
    # 计算相关性矩阵
    corr_matrix = metrics_df.corr()
    
    print("相关性矩阵：")
    print(corr_matrix.round(3))
    
    # 创建热力图
    plt.figure(figsize=(10, 8))
    
    # 创建掩码用于上三角
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    # 绘制热力图
    sns.heatmap(corr_matrix, 
                mask=mask,
                annot=True, 
                fmt='.2f', 
                cmap='coolwarm',
                center=0,
                square=True,
                linewidths=1,
                cbar_kws={"shrink": 0.8},
                annot_kws={"size": 12, "weight": "bold"})
    
    plt.title('关键生理指标相关性热力图（20个样本）', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('生理指标相关性热力图_20样本.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 打印相关性强弱说明
    print("\n相关性解释：")
    print("-" * 40)
    print("相关系数范围：-1 到 1")
    print("|r| > 0.7: 强相关")
    print("0.3 < |r| < 0.7: 中等相关")
    print("|r| < 0.3: 弱相关")
    
    # 找出强相关性对
    strong_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = abs(corr_matrix.iloc[i, j])
            if corr_value > 0.3:  # 由于样本量小，降低阈值
                strong_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))
    
    if strong_corr:
        print("\n发现中等及以上相关性：")
        for var1, var2, corr in strong_corr:
            direction = "正" if corr > 0 else "负"
            strength = "强" if abs(corr) > 0.7 else "中等"
            print(f"  {var1} 与 {var2}: {corr:.3f} ({direction}{strength}相关)")
    else:
        print("\n未发现中等以上相关性（样本量较小）")

# 4. 额外分析：数据分布概览
print("\n" + "="*60)
print("数据分布概览")
print("="*60)

# 创建分布图
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('糖尿病数据集分布概览（20个样本）', fontsize=16, fontweight='bold')

# 绘制每个数值变量的分布
numeric_cols = ['年龄', 'BMI', '血糖', '血压']
for idx, col in enumerate(numeric_cols):
    row = idx // 2
    col_pos = idx % 2
    
    # 直方图+KDE
    sns.histplot(data=df, x=col, kde=True, ax=axes[row, col_pos], bins=8)
    axes[row, col_pos].axvline(df[col].mean(), color='red', linestyle='--', linewidth=2, label=f'均值: {df[col].mean():.1f}')
    axes[row, col_pos].set_title(f'{col}分布', fontweight='bold')
    axes[row, col_pos].set_xlabel(col)
    axes[row, col_pos].set_ylabel('频数')
    axes[row, col_pos].legend()

# 患病状态分布饼图
outcome_counts = df['是否患病'].value_counts()
labels = ['健康', '患病']
colors_pie = ['lightgreen', 'lightcoral']

axes[0, 2].pie(outcome_counts.values, labels=labels, autopct='%1.1f%%', 
               colors=colors_pie, startangle=90, explode=(0.05, 0.05))
axes[0, 2].set_title('患病状态分布', fontweight='bold')

# BMI分类分布
bmi_counts = df['BMI分类'].value_counts()
axes[1, 2].bar(bmi_counts.index, bmi_counts.values, color=sns.color_palette('YlOrRd', len(bmi_counts)))
axes[1, 2].set_title('BMI分类分布', fontweight='bold')
axes[1, 2].set_xlabel('BMI分类')
axes[1, 2].set_ylabel('人数')

# 在每个条形上添加数值
for i, (index, value) in enumerate(bmi_counts.items()):
    axes[1, 2].text(i, value + 0.1, str(value), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('数据分布概览_20样本.png', dpi=300, bbox_inches='tight')
plt.show()

# 5. 生成详细的统计分析报告
print("\n" + "="*60)
print("详细的统计分析报告")
print("="*60)

# 按患病状态分组统计
print("\n按患病状态分组统计：")
print("-" * 50)
healthy_stats = df[df['是否患病'] == 0][['年龄', 'BMI', '血糖', '血压']].describe().round(2)
diabetic_stats = df[df['是否患病'] == 1][['年龄', 'BMI', '血糖', '血压']].describe().round(2)

print("健康组统计 (是否患病=0):")
print(healthy_stats)
print(f"\n样本数: {len(df[df['是否患病'] == 0])}")

print("\n\n患病组统计 (是否患病=1):")
print(diabetic_stats)
print(f"\n样本数: {len(df[df['是否患病'] == 1])}")

# 计算两组之间的差异
print("\n\n两组差异比较：")
print("-" * 50)
for col in ['年龄', 'BMI', '血糖', '血压']:
    healthy_mean = df[df['是否患病'] == 0][col].mean()
    diabetic_mean = df[df['是否患病'] == 1][col].mean()
    diff = diabetic_mean - healthy_mean
    diff_pct = (diff / healthy_mean * 100) if healthy_mean != 0 else 0
    
    print(f"{col}:")
    print(f"  健康组均值: {healthy_mean:.1f}")
    print(f"  患病组均值: {diabetic_mean:.1f}")
    print(f"  差异: {diff:+.1f} ({diff_pct:+.1f}%)")

# 6. 保存分析结果到CSV和Excel
print("\n" + "="*60)
print("保存分析结果")
print("="*60)

# 保存关键统计结果
analysis_results = {
    '总样本数': len(df),
    '健康人数': outcome_counts.get(0, 0),
    '患病人数': outcome_counts.get(1, 0),
    '患病率(%)': (outcome_counts.get(1, 0)/len(df)*100),
    '平均年龄': df['年龄'].mean(),
    '平均BMI': df['BMI'].mean(),
    '平均血糖': df['血糖'].mean(),
    '平均血压': df['血压'].mean(),
    'BMI-血糖相关系数': correlation,
    '数据生成时间': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
}

results_df = pd.DataFrame([analysis_results])
results_df.to_csv('糖尿病分析结果_20样本.csv', index=False, encoding='utf-8-sig')

# 保存详细数据
detailed_stats = pd.concat([
    df.describe().round(2),
    pd.DataFrame({'是否患病': df['是否患病'].value_counts()}).T
])
detailed_stats.to_excel('糖尿病详细统计_20样本.xlsx')

print(f"分析结果已保存到 '糖尿病分析结果_20样本.csv'")
print(f"详细统计已保存到 '糖尿病详细统计_20样本.xlsx'")

# 显示所有生成的文件
print("\n" + "="*60)
print("生成的文件列表")
print("="*60)
print("1. 糖尿病数据集_20样本.xlsx - 原始数据集")
print("2. 血糖_BMI_散点图_20样本.png - 散点图")
print("3. 年龄_患病率_分析_20样本.png - 箱线图和条形图")
print("4. 生理指标相关性热力图_20样本.png - 相关性热力图")
print("5. 数据分布概览_20样本.png - 数据分布概览")
print("6. 糖尿病分析结果_20样本.csv - 关键分析结果")
print("7. 糖尿病详细统计_20样本.xlsx - 详细统计分析")

# 显示数据集的简要描述
print("\n" + "="*60)
print("数据集简要描述")
print("="*60)
print(df[['患者ID', '年龄', 'BMI', '血糖', '血压', '是否患病']].to_string(index=False))