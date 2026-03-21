def calculate_salary_components(basic_salary: float, bonus: float = 0.0) -> dict:
    """
    Calculates salary components based on core formula:
    HRA = 20% of basic
    DA = 10% of basic
    PF = 5% deduction
    Net Salary = basic + hra + da + bonus - pf
    """
    hra = round(basic_salary * 0.20, 2)
    da = round(basic_salary * 0.10, 2)
    pf = round(basic_salary * 0.05, 2)
    net_salary = round(basic_salary + hra + da + bonus - pf, 2)
    
    return {
        "hra": hra,
        "da": da,
        "pf": pf,
        "net_salary": net_salary
    }
