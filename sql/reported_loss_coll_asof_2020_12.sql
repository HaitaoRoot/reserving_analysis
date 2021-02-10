select distinct
    acc_date.first_day_of_month as accident_month,
    asofdt.date_actual as as_of_month,
    DATEDIFF(month, accident_month, as_of_month)+1 AS development_age,
    dc.claim_id,
    df.claim_feature_id,
    case
        when symbol in ('uim','um') then 'umuim'
        when symbol in ('pd', 'umpd', 'uimpd') then 'pd'
        else symbol
    end as coverage,
    fla.reported_loss_dollar_amount as reported_loss
    
from edw.fact_loss_accumulating fla
    join edw.dim_coverage cov using(coverage_k)
    -- join claim and feature info - most recent information only
    join edw.dim_claim dc using(claim_k)
    join edw.dim_feature df using(feature_k)
    -- join dates
    join edw.dim_date acc_date on acc_date.date_k = dc.incident_date_k
    join edw.dim_date fnol_date on fnol_date.date_k = dc.fnol_date_k
    join edw.dim_date feat_date on feat_date.date_k = df.feature_opened_at_date_k
    -- join edw.dim_date asofdt on asofdt.date_k = fla.as_of_date_k
    join edw.dim_date asofdt on asofdt.date_k = fla.as_of_date_k and asofdt.last_day_of_month = asofdt.date_actual

where acc_date.date_actual between '2019-02-01' and (select max(date_actual) from edw.dim_date where day_closed = 'TRUE' and date_actual = last_day_of_month)
    and fnol_date.date_actual >= '2019-02-01' and feat_date.date_actual > '1900-01-01'
    and asofdt.date_actual <= '2020-12-31' 
    and coverage = 'coll'
order by 1,2,3