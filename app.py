import streamlit as st

st.set_page_config(
    page_title="Pakistan Salary Tax Calculator",
    page_icon="💰",
    layout="centered"
)


def calculate_annual_tax(annual_salary):

    slabs = [
        (0, 600000, 0.00),
        (600000, 1200000, 0.01),
        (1200000, 2200000, 0.11),
        (2200000, 3200000, 0.20),
        (3200000, 4100000, 0.25),
        (4100000, 5600000, 0.29),
        (5600000, 7000000, 0.32),
        (7000000, None, 0.35)
    ]

    total_tax = 0
    slab_details = []

    for lower, upper, rate in slabs:

        if annual_salary <= lower:
            break

        if upper is None:
            taxable_amount = annual_salary - lower
            slab_name = f"Above Rs. {lower:,.0f}"

        else:
            taxable_amount = min(annual_salary, upper) - lower
            slab_name = f"Rs. {lower:,.0f} to Rs. {upper:,.0f}"

        slab_tax = taxable_amount * rate
        total_tax += slab_tax

        slab_details.append({
            "slab": slab_name,
            "amount": taxable_amount,
            "rate": rate,
            "tax": slab_tax
        })

    return total_tax, slab_details


def find_gross_salary(net_annual_salary):

    low = net_annual_salary
    high = net_annual_salary * 2 + 1000000

    for _ in range(100):

        gross_salary = (low + high) / 2
        tax, _ = calculate_annual_tax(gross_salary)
        net_salary = gross_salary - tax

        if net_salary < net_annual_salary:
            low = gross_salary
        else:
            high = gross_salary

    return (low + high) / 2


st.title("💰 Pakistan Salary Tax Calculator")

st.write(
    "Calculate your estimated monthly salary, annual income tax "
    "and tax slab breakdown."
)

st.info(
    "This calculator uses the tax slabs in the original Python code. "
    "Please verify the applicable tax rates for the relevant tax year."
)

salary_type = st.selectbox(
    "Select your salary type",
    [
        "Annual Salary (Before Tax)",
        "Monthly Salary (After Tax)",
        "Monthly Salary (Before Tax)"
    ]
)

salary = st.number_input(
    "Enter salary amount (PKR)",
    min_value=0.0,
    value=50000.0,
    step=1000.0
)

if st.button("Calculate Tax", type="primary"):

    if salary_type == "Annual Salary (Before Tax)":
        annual_salary = salary

    elif salary_type == "Monthly Salary (After Tax)":
        annual_salary = find_gross_salary(salary * 12)

    else:
        annual_salary = salary * 12

    annual_tax, slab_details = calculate_annual_tax(annual_salary)

    monthly_salary_before_tax = annual_salary / 12
    monthly_tax = annual_tax / 12
    monthly_salary_after_tax = monthly_salary_before_tax - monthly_tax
    annual_salary_after_tax = annual_salary - annual_tax

    tax_percentage = (
        (annual_tax / annual_salary) * 100
        if annual_salary > 0 else 0
    )

    st.subheader("Salary Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Monthly Salary Before Tax",
            f"Rs. {monthly_salary_before_tax:,.2f}"
        )
        st.metric(
            "Monthly Tax Deduction",
            f"Rs. {monthly_tax:,.2f}"
        )
        st.metric(
            "Monthly Salary After Tax",
            f"Rs. {monthly_salary_after_tax:,.2f}"
        )

    with col2:
        st.metric(
            "Annual Salary Before Tax",
            f"Rs. {annual_salary:,.2f}"
        )
        st.metric(
            "Annual Income Tax",
            f"Rs. {annual_tax:,.2f}"
        )
        st.metric(
            "Annual Salary After Tax",
            f"Rs. {annual_salary_after_tax:,.2f}"
        )

    st.metric("Effective Tax Rate", f"{tax_percentage:.2f}%")

    st.subheader("Your Tax Slab Details")

    for i, detail in enumerate(slab_details, start=1):

        with st.expander(f"Slab {i}: {detail['slab']}"):

            st.write(
                f"Income in this slab: Rs. {detail['amount']:,.2f}"
            )

            st.write(
                f"Tax rate: {detail['rate'] * 100:.0f}%"
            )

            st.write(
                f"Tax on this slab: Rs. {detail['tax']:,.2f}"
            )

    st.subheader("Final Result")

    highest_slab = None

    for lower, upper, rate in [
        (0, 600000, 0.00),
        (600000, 1200000, 0.01),
        (1200000, 2200000, 0.11),
        (2200000, 3200000, 0.20),
        (3200000, 4100000, 0.25),
        (4100000, 5600000, 0.29),
        (5600000, 7000000, 0.32),
        (7000000, None, 0.35)
    ]:

        if annual_salary > lower:
            highest_slab = (lower, upper, rate)

    if highest_slab:

        lower, upper, rate = highest_slab

        if upper is None:
            st.write("Your salary falls in the slab above Rs. 7,000,000.")
        else:
            st.write(f"Your salary falls in the {rate * 100:.0f}% tax slab.")

        st.write(f"Marginal tax rate: {rate * 100:.0f}%")

    st.success(f"Total Annual Tax: Rs. {annual_tax:,.2f}")

    st.success(
        f"Annual Take-Home Salary: Rs. {annual_salary_after_tax:,.2f}"
    )