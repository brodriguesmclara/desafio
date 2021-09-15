CREATE OR REPLACE PROCEDURE dasa_bi.sp_cria_prestador()
BEGIN
CREATE OR REPLACE TABLE dasa_bi.Prestadores AS(
select 
     id_cnt as id_prt
     ,prestador 
from 
     dasa_bi.Contas 
group by 
     id_cnt,prestador 
order by 
     prestador asc);
END;