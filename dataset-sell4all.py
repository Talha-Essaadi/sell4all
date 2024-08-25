import pandas as pd
import matplotlib.pyplot as plt

# قائمة بأسماء الدول المعروفة
known_countries = [
    'United States', 'Canada', 'United Kingdom', 'France', 'Germany', 'Italy', 'Spain', 
    'Australia', 'Japan', 'China', 'India', 'Brazil', 'South Africa', 'Mexico', 'Argentina',
    'South Korea', 'Russia', 'Netherlands', 'Sweden', 'Norway', 'Denmark', 'USA', 'Finland', 
    'Greece', 'Turkey', 'Portugal', 'Switzerland', 'Belgium', 'Austria', 'Poland', 
    'Ireland', 'New Zealand', 'Singapore', 'Malaysia', 'Thailand', 'Philippines', 'UK', 'Vietnam',
    'Egypt', 'Saudi Arabia', 'United Arab Emirates', 'Israel', 'Jordan', 'Lebanon', 
    'Kuwait', 'Qatar', 'Oman', 'Bahrain', 'Pakistan', 'Bangladesh', 'Sri Lanka', 
    'Ukraine', 'Poland', 'Czech Republic', 'Hungary', 'Slovakia', 'Romania', 'Bulgaria', 
    'Croatia', 'Serbia', 'Bosnia and Herzegovina', 'Montenegro', 'North Macedonia', 
    'Albania', 'Lithuania', 'Latvia', 'Estonia', 'Belarus', 'Moldova', 'Georgia', 'Armenia', 
    'Azerbaijan', 'Kazakhstan', 'Uzbekistan', 'Turkmenistan', 'Kyrgyzstan', 'Tajikistan', 
    'Iraq', 'Syria', 'Yemen', 'Somalia', 'Sudan', 'Libya', 'Morocco', 'Tunisia', 
    'Algeria', 'Mauritania', 'Senegal', 'Ivory Coast', 'Ghana', 'Nigeria', 'Kenya', 
    'Ethiopia', 'Uganda', 'Rwanda', 'Burundi', 'Zambia', 'Zimbabwe', 'Botswana', 'Namibia', 
    'Lesotho', 'Swaziland', 'Malawi', 'Mozambique', 'Angola', 'DR Congo', 'Central African Republic',
    'Chad', 'Niger', 'Mali', 'Mauritania', 'Western Sahara', 'Cape Verde'
]

# تحميل البيانات من ملف CSV
data = pd.read_csv('dataset-sell4all.csv')

# تنظيف أسماء الأعمدة
data.columns = data.columns.str.strip()

# تحويل عمود 'Age' و 'Dépenses des clients' إلى القيم الرقمية
data['Age'] = pd.to_numeric(data['Age'], errors='coerce')
data['Dépenses des clients'] = pd.to_numeric(data['Dépenses des clients'], errors='coerce')

# إزالة الصفوف التي تحتوي على قيم مفقودة في عمود 'Age' و 'Dépenses des clients'
data_cleaned = data.dropna(subset=['Age', 'Dépenses des clients'])

# تصفية عمود 'Pays' بحيث يحتوي فقط على أسماء الدول المعروفة
data_cleaned['Pays'] = data_cleaned['Pays'].apply(lambda x: x if x in known_countries else None)

# إزالة الصفوف التي تحتوي على أسماء دول غير معروفة
data_cleaned = data_cleaned[data_cleaned['Pays'].notna()]

# عرض قائمة بأسماء الدول فقط بعد التنظيف
unique_countries = data_cleaned['Pays'].unique()
print(unique_countries)

# إزالة الصفوف التي تحتوي على إنفاق أقل من 10 يورو
data_cleaned = data_cleaned[data_cleaned['Dépenses des clients'] >= 10]

# إزالة التكرارات
data_cleaned = data_cleaned.drop_duplicates()

# حساب متوسط ووسيط العمر بعد تنظيف البيانات
mean_age = data_cleaned['Age'].mean()
median_age = data_cleaned['Age'].median()
mean_spending = data_cleaned['Dépenses des clients'].mean()
median_spending = data_cleaned['Dépenses des clients'].median()

# عرض النتائج مع تنسيق الأرقام
print(f"Âge moyen : {mean_age:.2f}")
print(f"Âge médian : {median_age:.2f}")
print(f"Dépenses moyennes : {mean_spending:.2f}")
print(f"Dépenses médianes : {median_spending:.2f}")

# إعداد البيانات لرسم المبيان
data_grouped = data_cleaned.groupby('Pays')['Dépenses des clients'].sum()
data_grouped_sorted = data_grouped.sort_values(ascending=False)  # فرز القيم من الأكبر إلى الأصغر

# إنشاء رسم بياني يوضح الإنفاق حسب البلد
plt.figure(figsize=(12, 8))
data_grouped_sorted.plot(kind='bar')
plt.title('Dépenses totales par pays')
plt.xlabel('Pays')
plt.ylabel('Dépenses totales (€)')
plt.xticks(rotation=45)
plt.show()

# كتابة البيانات النظيفة إلى ملف CSV جديد
data_cleaned.to_csv('6-sell4all.csv', columns=['Pays', 'Age', 'Genre', 'Dépenses des clients'], index=False)