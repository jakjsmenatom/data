SELECT
    c.id_alp3 AS country_id_alp3,
    c.name AS country_name,
    2020 AS year,
    hdp.value AS hdp,
    hdp_na_obyvatele.value AS hdp_na_obyvatele,
    hdp_mezirocni_rust_procentualne.value AS hdp_mezirocni_rust_procentualne,
    inflace_index_spotrebitelskych_cen_mezirocne.value AS inflace_index_spotrebitelskych_cen_mezirocne,
    nezamestnanost_procento.value AS nezamestnanost_procento,
    statni_dluh_centralni_vlady_procento_hdp.value AS statni_dluh_centralni_vlady_procento_hdp,
    zadluzeni_soukromeho_sektoru_procento_hdp.value AS zadluzeni_soukromeho_sektoru_procento_hdp
FROM countries AS c
    JOIN imf.hdp ON c.id_alp3 = hdp.country_id_alp3
    JOIN imf.hdp_na_obyvatele ON c.id_alp3 = hdp_na_obyvatele.country_id_alp3
    JOIN imf.hdp_mezirocni_rust_procentualne ON c.id_alp3 = hdp_mezirocni_rust_procentualne.country_id_alp3
    JOIN imf.inflace_index_spotrebitelskych_cen_mezirocne ON c.id_alp3 = inflace_index_spotrebitelskych_cen_mezirocne.country_id_alp3
    JOIN imf.nezamestnanost_procento ON c.id_alp3 = nezamestnanost_procento.country_id_alp3
    JOIN imf.statni_dluh_centralni_vlady_procento_hdp ON c.id_alp3 = statni_dluh_centralni_vlady_procento_hdp.country_id_alp3
    JOIN imf.zadluzeni_soukromeho_sektoru_procento_hdp ON c.id_alp3 = zadluzeni_soukromeho_sektoru_procento_hdp.country_id_alp3
WHERE
    hdp.year = 2020 AND
    hdp_na_obyvatele.year = 2020 AND
    hdp_mezirocni_rust_procentualne.year = 2020 AND
    inflace_index_spotrebitelskych_cen_mezirocne.year = 2020 AND
    nezamestnanost_procento.year = 2020 AND
    statni_dluh_centralni_vlady_procento_hdp.year = 2020 AND
    zadluzeni_soukromeho_sektoru_procento_hdp.year = 2020
;
