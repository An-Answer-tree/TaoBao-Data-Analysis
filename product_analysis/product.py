import pandas as pd
import streamlit as st 
import plotly.express as px

# 使DataFrame在jupyter notebook中输出不换行
pd.set_option('display.expand_frame_repr', False)
df = pd.read_csv('../user_action_after_preprocess.csv')

# 设置网页信息 
st.set_page_config(page_title="商品流量数据大屏", page_icon=":bar_chart:", layout="wide")

# 侧边栏
st.sidebar.header("请在这里筛选:")

item_category = st.sidebar.multiselect(
    "选择商品种类:",
    options=df["item_category"].unique(),
    default= None
)

behavior_type = st.sidebar.multiselect(
    "选择用户行为:",
    options=df["behavior_type"].unique(),
    default= None
)

df_selection = df.query("item_category == @item_category & behavior_type == @behavior_type ")

# 主页面
st.title(":bar_chart: 流量数据大屏")
st.markdown("##")
 
# 核心指标, 销售总额、平均评分、星级、平均销售额数据
total_sales = int(df_selection.shape[0])
# average_rating = round(df_selection["评分"].mean(), 1)
# star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = total_sales // 31
 
# 3列布局
left_column, middle_column, right_column = st.columns(3)
 
# 添加相关信息
with left_column:
    st.subheader("商品总流量:")
    st.subheader(f"SUM {total_sales:,}")
# with middle_column:
#     st.subheader("平均评分:")
#     st.subheader(f"{average_rating} {star_rating}")
with middle_column:
    st.subheader("日平均流量:")
    st.subheader(f"AVERAGE {average_sale_by_transaction}")
 
# 分隔符
st.markdown("""---""")

# 每日流量情况(柱状图)
sales_by_day = df_selection.groupby(by=["date"]).size()
# 将索引转换为日期格式，指定日期格式为"月份-日期"
sales_by_day.index = pd.to_datetime(sales_by_day.index, format="%m-%d")
# 在索引前添加年份"2014"
sales_by_day.index = "2014-" + sales_by_day.index.strftime("%m-%d")

fig_daily_sales = px.bar(
    x=sales_by_day.index,
    y=sales_by_day.values,
    title="每日总流量",
    color_discrete_sequence=["#0083B8"],
    template="plotly_white"
)
fig_daily_sales.update_layout(
    xaxis_title="日期",  # 设置X轴标题
    yaxis_title="总流量",  # 设置Y轴标题
    xaxis_tickangle=45,
    yaxis=dict(
        gridcolor="lightgray"
    ),
    xaxis=dict(
        automargin=True,  # 自动调整图表大小以适应较长的横轴
        tickmode="linear"
    ),
    hovermode="x",  # 设置鼠标悬停模式为沿X轴
)
 
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_daily_sales, use_container_width=True)
# right_column.plotly_chart(fig_product_sales, use_container_width=True)
