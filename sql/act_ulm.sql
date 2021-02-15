select
    m.first_day_of_month as exposure_month,
    ffa.as_of_date_k as as_of_month,
    development_age_in_months,
    case
        when symbol in ('uim','um') then 'umuim'
        when symbol in ('pd', 'umpd', 'uimpd') then 'pd'
        else symbol
    end as coverage,

    -- this is ultimate loss, net of salvage and subrogation
    sum(ffa.actuarial_ibner_dollar_amount + ffa.actuarial_pure_ibnr_dollar_amount + ffa.reported_loss_dollar_amount) as act_ultimate_loss

 
from edw.fact_financials_accumulating ffa

-- cov.symbol has the coverage name
join edw.dim_coverage cov using (coverage_k)
join edw.dim_month m on m.month_k = ffa.exposure_month_k
join edw.dim_date asofdt on asofdt.date_k = ffa.as_of_date_k


where 
    -- m.first_day_of_month between '2019-02-01' and '2020-12-01'
    -- and asofdt.date_actual <= '2020-12-31'
    m.first_day_of_month between '2019-02-01' and 'para_asofdate'
    and asofdt.date_actual <= 'para_asofdate'
    and coverage = 'para_cov'
    
group by 1,2,3,4
having sum(earned_premium_dollar_amount) > 0
order by 1,2,3,4