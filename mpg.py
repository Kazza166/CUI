import streamlit as st

st.title("UK Carer Benefits Eligibility Checker")
st.write("""
This tool helps unpaid carers in the UK identify potential benefits and entitlements based on their circumstances.
Please provide accurate information for the most relevant results.
""")

# Input sections
st.header("Personal Details")

age = st.number_input("Your Age", min_value=0, max_value=120, value=30)
state_pension_age = st.radio("Have you reached State Pension age?", ("No", "Yes"))
full_time_education = st.radio("Are you in full-time education (21 hours or more per week)?", ("No", "Yes"))
employment_status = st.selectbox("Employment Status", ("Employed", "Self-employed", "Unemployed", "Retired"))
weekly_earnings = st.number_input("Your Net Weekly Earnings (£)", min_value=0.0, value=0.0)
savings = st.number_input("Your Total Savings (£)", min_value=0.0, value=0.0)
on_means_tested_benefits = st.radio("Are you currently receiving any means-tested benefits?", ("No", "Yes"))

st.header("Caring Details")

hours_caring = st.number_input("Hours Spent Caring per Week", min_value=0, max_value=168, value=35)
lives_with_cared = st.radio("Do you live with the person you care for?", ("No", "Yes"))
relationship_to_cared = st.selectbox("Relationship to the Person Cared For", ("Spouse/Partner", "Child under 18", "Other"))
cared_receives_benefit = st.radio("Does the person you care for receive a qualifying disability benefit?", ("No", "Yes"))
cared_age = st.number_input("Age of the Person Cared For", min_value=0, max_value=120, value=70)
cared_has_disability = st.radio("Does the person you care for have a disability or long-term health condition?", ("Yes", "No"))

st.header("Housing Details")

paying_rent = st.radio("Are you paying rent?", ("No", "Yes"))
paying_council_tax = st.radio("Are you responsible for Council Tax?", ("No", "Yes"))

st.header("Health and Disability")

has_disability = st.radio("Do you have a disability or health condition affecting your ability to work?", ("No", "Yes"))
veteran = st.radio("Are you or the person you care for a military veteran?", ("No", "Yes"))

st.header("Additional Details")

water_meter = st.radio("Do you have a water meter installed?", ("No", "Yes"))
high_water_use = st.radio("Do you have high essential water use due to medical conditions?", ("No", "Yes"))
childcare_responsibilities = st.radio("Do you have childcare responsibilities?", ("No", "Yes"))
income_support_criteria = st.radio("Do you meet the criteria for Income Support (e.g., pregnant, carer, single parent with child under 5)?", ("No", "Yes"))
young_carer = st.radio("Are you a young carer under the age of 18?", ("No", "Yes"))
savings_over_16000 = savings >= 16000

# Determine eligibility
st.header("Potential Eligible Benefits")

eligible_benefits = []

# 1. Carer's Allowance
if (
    hours_caring >= 35
    and cared_receives_benefit == "Yes"
    and weekly_earnings <= 139
    and full_time_education == "No"
    and state_pension_age == "No"
):
    eligible_benefits.append("Carer's Allowance")

# 2. Carer's Credit
if (
    hours_caring >= 20
    and (cared_receives_benefit == "Yes" or cared_has_disability == "Yes")
    and age >= 16
    and state_pension_age == "No"
):
    eligible_benefits.append("Carer's Credit")

# 3. Universal Credit
if (
    state_pension_age == "No"
    and savings < 16000
    and employment_status != "Retired"
    and (on_means_tested_benefits == "Yes" or weekly_earnings < 1000)
):
    eligible_benefits.append("Universal Credit (with Carer Element)")

# 4. Income Support
if (
    state_pension_age == "No"
    and income_support_criteria == "Yes"
    and savings < 16000
    and employment_status != "Employed"
):
    eligible_benefits.append("Income Support")

# 5. Pension Credit
if state_pension_age == "Yes" and savings < 10000:
    eligible_benefits.append("Pension Credit (with Carer Addition)")

# 6. Council Tax Reduction and Discounts
if (
    paying_council_tax == "Yes"
    and lives_with_cared == "Yes"
    and relationship_to_cared != "Spouse/Partner"
    and hours_caring >= 35
):
    eligible_benefits.append("Council Tax Reduction/Discount")

# 7. Housing Benefit
if (
    paying_rent == "Yes"
    and savings < 16000
    and employment_status != "Employed"
    and state_pension_age == "No"
):
    eligible_benefits.append("Housing Benefit")

# 8. Disability Benefits for the Person Cared For
if cared_has_disability == "Yes":
    if cared_age >= 16 and cared_age < 66:
        eligible_benefits.append("Personal Independence Payment (PIP) for the person you care for")
    elif cared_age < 16:
        eligible_benefits.append("Disability Living Allowance (DLA) for the person you care for")
    elif cared_age >= 66:
        eligible_benefits.append("Attendance Allowance for the person you care for")

# 9. Blue Badge Scheme
if cared_has_disability == "Yes":
    eligible_benefits.append("Blue Badge Scheme")

# 10. Disabled Facilities Grant
if cared_has_disability == "Yes" and lives_with_cared == "Yes":
    eligible_benefits.append("Disabled Facilities Grant")

# 11. Carer's Assessment
eligible_benefits.append("Carer's Assessment by Local Council")

# 12. Respite Care and Short Breaks
eligible_benefits.append("Respite Care and Short Breaks")

# 13. Employment Rights for Carers
if employment_status in ["Employed", "Self-employed"]:
    eligible_benefits.append("Employment Rights: Flexible Working Requests, Time Off for Dependants")

# 14. Training and Education Opportunities
eligible_benefits.append("Training and Education Opportunities")

# 15. Grants and Financial Assistance
if savings < 16000:
    eligible_benefits.append("Grants and Financial Assistance from Charities")

# 16. Health and Wellbeing Support
eligible_benefits.append("Health and Wellbeing Support Services")
if has_disability == "Yes":
    eligible_benefits.append("Employment and Support Allowance (ESA)")
    eligible_benefits.append("Free NHS Prescriptions and Health Costs (subject to eligibility)")

# 17. Legal Rights and Advocacy
eligible_benefits.append("Legal Rights and Advocacy Services")

# 18. Utility Bill Discounts
if on_means_tested_benefits == "Yes":
    eligible_benefits.append("Warm Home Discount Scheme")
if water_meter == "Yes" and high_water_use == "Yes" and on_means_tested_benefits == "Yes":
    eligible_benefits.append("WaterSure Scheme")
eligible_benefits.append("Priority Services Register for Utilities")

# 19. Disabled Persons Railcard
if cared_has_disability == "Yes":
    eligible_benefits.append("Disabled Persons Railcard")

# 20. Motability Scheme
if cared_has_disability == "Yes" and cared_receives_benefit == "Yes":
    eligible_benefits.append("Motability Scheme")

# 21. Support from Charities and Organizations
eligible_benefits.append("Support from Carers UK, Carers Trust, and other organizations")

# 22. Young Carers Support
if young_carer == "Yes":
    eligible_benefits.append("Support for Young Carers: Assessments, Educational Support, Respite Activities")

# 23. Free Flu Vaccinations
eligible_benefits.append("Free Flu Vaccinations for Carers")

# 24. Veteran Support Services
if veteran == "Yes":
    eligible_benefits.append("Priority NHS Treatment for Veterans")

# Display results
if eligible_benefits:
    st.success("Based on the information provided, you may be eligible for the following benefits and support:")
    for benefit in sorted(set(eligible_benefits)):
        st.write(f"- **{benefit}**")
else:
    st.info("You may not be eligible for specific carer benefits based on the provided information. Consider seeking advice from a professional benefits advisor.")

# Additional resources
st.header("Additional Resources")
st.write("""
- [GOV.UK Benefits Information](https://www.gov.uk/browse/benefits)
- [Carers' Resource](https://www.carersresource.org/)
- [Citizens Advice](https://www.citizensadvice.org.uk/)
- [Turn2us Benefits Calculator](https://benefits-calculator.turn2us.org.uk/)
""")

st.write("Please note that this tool provides a general guide and should not be considered as legal or financial advice. For personalized advice, consult official government resources or a professional advisor.")
