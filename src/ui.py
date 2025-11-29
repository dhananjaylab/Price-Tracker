import streamlit as st
import requests
import pandas as pd
import time

# --- CONFIG ---
API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Amazon Tracker", page_icon="🛒", layout="wide")

# --- CSS STYLING ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (ADD PRODUCT) ---
with st.sidebar:
    st.header("➕ Add New Product")
    with st.form("add_product_form", clear_on_submit=True):
        title = st.text_input("Product Name", placeholder="e.g. iPhone 15")
        url = st.text_input("Amazon URL")
        target = st.number_input("Target Price (₹)", min_value=1.0, step=100.0)
        submitted = st.form_submit_button("Track Product")
        
        if submitted and url and target:
            try:
                payload = {"title": title, "url": url, "target_price": target}
                res = requests.post(f"{API_URL}/products", json=payload)
                if res.status_code == 200:
                    st.success("Product added!")
                    time.sleep(1)
                    st.rerun()
                elif res.status_code == 400:
                    st.warning("Product already exists!")
                else:
                    st.error("Could not add product.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# --- MAIN PAGE ---
st.title("🛒 Amazon Price Tracker Dashboard")

# Top Stats Row
try:
    stats_req = requests.get(f"{API_URL}/stats")
    if stats_req.status_code == 200:
        stats = stats_req.json()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Products", stats.get('total_products', 0))
        col2.metric("Total Scans", stats.get('total_price_checks', 0))
        
        if st.button("⚡ Trigger Manual Scan"):
            requests.post(f"{API_URL}/trigger-scan")
            st.toast("Background scan started!", icon="🤖")
    else:
        st.error("Backend API is not running!")
        st.stop()
except:
    st.error("Cannot connect to Backend API. Is it running on port 8000?")
    st.stop()

st.divider()

# --- MAIN DATA TABLE ---
st.subheader("📦 Tracked Items")

products_req = requests.get(f"{API_URL}/products")
if products_req.status_code == 200:
    products = products_req.json()
    
    if products:
        # Convert to DataFrame for nicer table
        df = pd.DataFrame(products)
        
        # UI Layout per product using Expanders
        for index, row in df.iterrows():
            last_price = row['last_price'] if row['last_price'] else 0
            target = row['target_price']
            
            # Determine Color Status
            if last_price > 0 and last_price <= target:
                status_color = "🟢 **BUY NOW!**"
            elif last_price == 0:
                status_color = "🟡 Checking..."
            else:
                status_color = "🔴 Watch"

            with st.expander(f"{status_color} {row['title']} - ₹{last_price} (Target: ₹{target})"):
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    st.caption(f"Last Checked: {row.get('last_check', 'Never')}")
                    st.markdown(f"[View on Amazon]({row['url']})")
                    
                    # Fetch History for Chart
                    hist_req = requests.get(f"{API_URL}/products/{row['id']}/history")
                    if hist_req.status_code == 200:
                        hist_data = hist_req.json()
                        if hist_data:
                            hist_df = pd.DataFrame(hist_data)
                            hist_df['timestamp'] = pd.to_datetime(hist_df['timestamp'])
                            st.line_chart(hist_df, x='timestamp', y='price')
                        else:
                            st.info("No price history yet.")

                with c2:
                    st.metric("Current Price", f"₹{last_price}", delta=f"{target - last_price} vs Target")
                    if st.button("Stop Tracking", key=f"del_{row['id']}"):
                        requests.delete(f"{API_URL}/products/{row['id']}")
                        st.rerun()
    else:
        st.info("No products tracked yet. Add one via the sidebar!")

# Auto-refresh mechanism (every 60 seconds)
if st.checkbox("Auto-refresh data (60s)", value=True):
    time.sleep(60)
    st.rerun()
