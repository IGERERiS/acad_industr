# coding=utf8
# Aim of this program is to retrieve data from the databases
# and to print the graphs for the paper
# Data available for the period: 1982-2019
# By default we plot graphs for the 1990-2019
# Databases available for SEG, EAGE and SPE
# Timofey Eltsov
# April 12, 2020
import itertools
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.ticker import NullFormatter
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import numpy
import sqlite3
import time
import ssl
import ast
from PIL import Image
# France crude oil production, 1960 - 2019, thousand+bpd+oil
# For the 2019 data is available only fo 9 months
france_cop = [36.4418, 40.4553, 44.1147, 47.3019, 52.968, 55.9191, 54.6206, 53.3221, 50.489, 47.0658, 44.2327, 34.9073, 27.8246, 23.457, 20.1518, 19.2074, 19.9157, 19.9157, 19.9157, 19.9157, 25.3457, 29.5953, 34.9073, 34.9073, 34.9073, 50.6071, 58.7521, 63.828, 67.3693, 65.0084, 60.5228, 59.1062, 57.2175, 55.2108, 55.3288, 50.0169, 42.1079, 35.7336, 34.0809, 30.7757, 28.1788, 27.7066, 26.2901, 24.4013, 22.7487, 21.5683, 21.3322, 19.4435, 19.4435, 18.145, 18.027, 17.7909, 16.1383, 15.9022, 15.1939, 16.6105, 16.3744, 15.0759, 15.5481, 14.40444444] 

years = []
start_year = 1982
end_year = 2019
fontsize_det = 13


countr_dict = {"Afghanistan" : {'Alpha-2': 'AF', 'Alpha-3': 'AFG', 'Numeric code': '004', 'Link to ISO 3166-2': 'ISO 3166-2:AF', 'Independent': 'Yes'},
"Åland Islands" : {'Alpha-2': 'AX', 'Alpha-3': 'ALA', 'Numeric code': '248', 'Link to ISO 3166-2': 'ISO 3166-2:AX', 'Independent': 'No'},
"Albania" : {'Alpha-2': 'AL', 'Alpha-3': 'ALB', 'Numeric code': '008', 'Link to ISO 3166-2': 'ISO 3166-2:AL', 'Independent': 'Yes'},
"Algeria" : {'Alpha-2': 'DZ', 'Alpha-3': 'DZA', 'Numeric code': '012', 'Link to ISO 3166-2': 'ISO 3166-2:DZ', 'Independent': 'Yes'},
"American Samoa" : {'Alpha-2': 'AS', 'Alpha-3': 'ASM', 'Numeric code': '016', 'Link to ISO 3166-2': 'ISO 3166-2:AS', 'Independent': 'No'},
"Andorra" : {'Alpha-2': 'AD', 'Alpha-3': 'AND', 'Numeric code': '020', 'Link to ISO 3166-2': 'ISO 3166-2:AD', 'Independent': 'Yes'},
"Angola" : {'Alpha-2': 'AO', 'Alpha-3': 'AGO', 'Numeric code': '024', 'Link to ISO 3166-2': 'ISO 3166-2:AO', 'Independent': 'Yes'},
"Anguilla" : {'Alpha-2': 'AI', 'Alpha-3': 'AIA', 'Numeric code': '660', 'Link to ISO 3166-2': 'ISO 3166-2:AI', 'Independent': 'No'},
"Antarctica" : {'Alpha-2': 'AQ', 'Alpha-3': 'ATA', 'Numeric code': '010', 'Link to ISO 3166-2': 'ISO 3166-2:AQ', 'Independent': 'No'},
"Antigua and Barbuda" : {'Alpha-2': 'AG', 'Alpha-3': 'ATG', 'Numeric code': '028', 'Link to ISO 3166-2': 'ISO 3166-2:AG', 'Independent': 'Yes'},
"Argentina" : {'Alpha-2': 'AR', 'Alpha-3': 'ARG', 'Numeric code': '032', 'Link to ISO 3166-2': 'ISO 3166-2:AR', 'Independent': 'Yes'},
"Armenia" : {'Alpha-2': 'AM', 'Alpha-3': 'ARM', 'Numeric code': '051', 'Link to ISO 3166-2': 'ISO 3166-2:AM', 'Independent': 'Yes'},
"Aruba" : {'Alpha-2': 'AW', 'Alpha-3': 'ABW', 'Numeric code': '533', 'Link to ISO 3166-2': 'ISO 3166-2:AW', 'Independent': 'No'},
"Australia" : {'Alpha-2': 'AU', 'Alpha-3': 'AUS', 'Numeric code': '036', 'Link to ISO 3166-2': 'ISO 3166-2:AU', 'Independent': 'Yes'},
"Austria" : {'Alpha-2': 'AT', 'Alpha-3': 'AUT', 'Numeric code': '040', 'Link to ISO 3166-2': 'ISO 3166-2:AT', 'Independent': 'Yes'},
"Azerbaijan" : {'Alpha-2': 'AZ', 'Alpha-3': 'AZE', 'Numeric code': '031', 'Link to ISO 3166-2': 'ISO 3166-2:AZ', 'Independent': 'Yes'},
"Bahamas" : {'Alpha-2': 'BS', 'Alpha-3': 'BHS', 'Numeric code': '044', 'Link to ISO 3166-2': 'ISO 3166-2:BS', 'Independent': 'Yes'},
"Bahrain" : {'Alpha-2': 'BH', 'Alpha-3': 'BHR', 'Numeric code': '048', 'Link to ISO 3166-2': 'ISO 3166-2:BH', 'Independent': 'Yes'},
"Bangladesh" : {'Alpha-2': 'BD', 'Alpha-3': 'BGD', 'Numeric code': '050', 'Link to ISO 3166-2': 'ISO 3166-2:BD', 'Independent': 'Yes'},
"Barbados" : {'Alpha-2': 'BB', 'Alpha-3': 'BRB', 'Numeric code': '052', 'Link to ISO 3166-2': 'ISO 3166-2:BB', 'Independent': 'Yes'},
"Belarus" : {'Alpha-2': 'BY', 'Alpha-3': 'BLR', 'Numeric code': '112', 'Link to ISO 3166-2': 'ISO 3166-2:BY', 'Independent': 'Yes'},
"Belgium" : {'Alpha-2': 'BE', 'Alpha-3': 'BEL', 'Numeric code': '056', 'Link to ISO 3166-2': 'ISO 3166-2:BE', 'Independent': 'Yes'},
"Belize" : {'Alpha-2': 'BZ', 'Alpha-3': 'BLZ', 'Numeric code': '084', 'Link to ISO 3166-2': 'ISO 3166-2:BZ', 'Independent': 'Yes'},
"Benin" : {'Alpha-2': 'BJ', 'Alpha-3': 'BEN', 'Numeric code': '204', 'Link to ISO 3166-2': 'ISO 3166-2:BJ', 'Independent': 'Yes'},
"Bermuda" : {'Alpha-2': 'BM', 'Alpha-3': 'BMU', 'Numeric code': '060', 'Link to ISO 3166-2': 'ISO 3166-2:BM', 'Independent': 'No'},
"Bhutan" : {'Alpha-2': 'BT', 'Alpha-3': 'BTN', 'Numeric code': '064', 'Link to ISO 3166-2': 'ISO 3166-2:BT', 'Independent': 'Yes'},
"Bolivia (Plurinational State of)" : {'Alpha-2': 'BO', 'Alpha-3': 'BOL', 'Numeric code': '068', 'Link to ISO 3166-2': 'ISO 3166-2:BO', 'Independent': 'Yes'},
"Bonaire, Sint Eustatius and Saba" : {'Alpha-2': 'BQ', 'Alpha-3': 'BES', 'Numeric code': '535', 'Link to ISO 3166-2': 'ISO 3166-2:BQ', 'Independent': 'No'},
"Bosnia and Herzegovina" : {'Alpha-2': 'BA', 'Alpha-3': 'BIH', 'Numeric code': '070', 'Link to ISO 3166-2': 'ISO 3166-2:BA', 'Independent': 'Yes'},
"Botswana" : {'Alpha-2': 'BW', 'Alpha-3': 'BWA', 'Numeric code': '072', 'Link to ISO 3166-2': 'ISO 3166-2:BW', 'Independent': 'Yes'},
"Bouvet Island" : {'Alpha-2': 'BV', 'Alpha-3': 'BVT', 'Numeric code': '074', 'Link to ISO 3166-2': 'ISO 3166-2:BV', 'Independent': 'No'},
"Brazil" : {'Alpha-2': 'BR', 'Alpha-3': 'BRA', 'Numeric code': '076', 'Link to ISO 3166-2': 'ISO 3166-2:BR', 'Independent': 'Yes'},
"British Indian Ocean Territory" : {'Alpha-2': 'IO', 'Alpha-3': 'IOT', 'Numeric code': '086', 'Link to ISO 3166-2': 'ISO 3166-2:IO', 'Independent': 'No'},
"Brunei Darussalam" : {'Alpha-2': 'BN', 'Alpha-3': 'BRN', 'Numeric code': '096', 'Link to ISO 3166-2': 'ISO 3166-2:BN', 'Independent': 'Yes'},
"Bulgaria" : {'Alpha-2': 'BG', 'Alpha-3': 'BGR', 'Numeric code': '100', 'Link to ISO 3166-2': 'ISO 3166-2:BG', 'Independent': 'Yes'},
"Burkina Faso" : {'Alpha-2': 'BF', 'Alpha-3': 'BFA', 'Numeric code': '854', 'Link to ISO 3166-2': 'ISO 3166-2:BF', 'Independent': 'Yes'},
"Burundi" : {'Alpha-2': 'BI', 'Alpha-3': 'BDI', 'Numeric code': '108', 'Link to ISO 3166-2': 'ISO 3166-2:BI', 'Independent': 'Yes'},
"Cabo Verde" : {'Alpha-2': 'CV', 'Alpha-3': 'CPV', 'Numeric code': '132', 'Link to ISO 3166-2': 'ISO 3166-2:CV', 'Independent': 'Yes'},
"Cambodia" : {'Alpha-2': 'KH', 'Alpha-3': 'KHM', 'Numeric code': '116', 'Link to ISO 3166-2': 'ISO 3166-2:KH', 'Independent': 'Yes'},
"Cameroon" : {'Alpha-2': 'CM', 'Alpha-3': 'CMR', 'Numeric code': '120', 'Link to ISO 3166-2': 'ISO 3166-2:CM', 'Independent': 'Yes'},
"Canada" : {'Alpha-2': 'CA', 'Alpha-3': 'CAN', 'Numeric code': '124', 'Link to ISO 3166-2': 'ISO 3166-2:CA', 'Independent': 'Yes'},
"Cayman Islands" : {'Alpha-2': 'KY', 'Alpha-3': 'CYM', 'Numeric code': '136', 'Link to ISO 3166-2': 'ISO 3166-2:KY', 'Independent': 'No'},
"Central African Republic" : {'Alpha-2': 'CF', 'Alpha-3': 'CAF', 'Numeric code': '140', 'Link to ISO 3166-2': 'ISO 3166-2:CF', 'Independent': 'Yes'},
"Chad" : {'Alpha-2': 'TD', 'Alpha-3': 'TCD', 'Numeric code': '148', 'Link to ISO 3166-2': 'ISO 3166-2:TD', 'Independent': 'Yes'},
"Chile" : {'Alpha-2': 'CL', 'Alpha-3': 'CHL', 'Numeric code': '152', 'Link to ISO 3166-2': 'ISO 3166-2:CL', 'Independent': 'Yes'},
"China" : {'Alpha-2': 'CN', 'Alpha-3': 'CHN', 'Numeric code': '156', 'Link to ISO 3166-2': 'ISO 3166-2:CN', 'Independent': 'Yes'},
"Christmas Island" : {'Alpha-2': 'CX', 'Alpha-3': 'CXR', 'Numeric code': '162', 'Link to ISO 3166-2': 'ISO 3166-2:CX', 'Independent': 'No'},
"Cocos (Keeling) Islands" : {'Alpha-2': 'CC', 'Alpha-3': 'CCK', 'Numeric code': '166', 'Link to ISO 3166-2': 'ISO 3166-2:CC', 'Independent': 'No'},
"Colombia" : {'Alpha-2': 'CO', 'Alpha-3': 'COL', 'Numeric code': '170', 'Link to ISO 3166-2': 'ISO 3166-2:CO', 'Independent': 'Yes'},
"Comoros" : {'Alpha-2': 'KM', 'Alpha-3': 'COM', 'Numeric code': '174', 'Link to ISO 3166-2': 'ISO 3166-2:KM', 'Independent': 'Yes'},
"Congo" : {'Alpha-2': 'CG', 'Alpha-3': 'COG', 'Numeric code': '178', 'Link to ISO 3166-2': 'ISO 3166-2:CG', 'Independent': 'Yes'},
"Congo, Democratic Republic of the" : {'Alpha-2': 'CD', 'Alpha-3': 'COD', 'Numeric code': '180', 'Link to ISO 3166-2': 'ISO 3166-2:CD', 'Independent': 'Yes'},
"Cook Islands" : {'Alpha-2': 'CK', 'Alpha-3': 'COK', 'Numeric code': '184', 'Link to ISO 3166-2': 'ISO 3166-2:CK', 'Independent': 'No'},
"Costa Rica" : {'Alpha-2': 'CR', 'Alpha-3': 'CRI', 'Numeric code': '188', 'Link to ISO 3166-2': 'ISO 3166-2:CR', 'Independent': 'Yes'},
"Côte d'Ivoire" : {'Alpha-2': 'CI', 'Alpha-3': 'CIV', 'Numeric code': '384', 'Link to ISO 3166-2': 'ISO 3166-2:CI', 'Independent': 'Yes'},
"Croatia" : {'Alpha-2': 'HR', 'Alpha-3': 'HRV', 'Numeric code': '191', 'Link to ISO 3166-2': 'ISO 3166-2:HR', 'Independent': 'Yes'},
"Cuba" : {'Alpha-2': 'CU', 'Alpha-3': 'CUB', 'Numeric code': '192', 'Link to ISO 3166-2': 'ISO 3166-2:CU', 'Independent': 'Yes'},
"Curaçao" : {'Alpha-2': 'CW', 'Alpha-3': 'CUW', 'Numeric code': '531', 'Link to ISO 3166-2': 'ISO 3166-2:CW', 'Independent': 'No'},
"Cyprus" : {'Alpha-2': 'CY', 'Alpha-3': 'CYP', 'Numeric code': '196', 'Link to ISO 3166-2': 'ISO 3166-2:CY', 'Independent': 'Yes'},
"Czechia" : {'Alpha-2': 'CZ', 'Alpha-3': 'CZE', 'Numeric code': '203', 'Link to ISO 3166-2': 'ISO 3166-2:CZ', 'Independent': 'Yes'},
"Denmark" : {'Alpha-2': 'DK', 'Alpha-3': 'DNK', 'Numeric code': '208', 'Link to ISO 3166-2': 'ISO 3166-2:DK', 'Independent': 'Yes'},
"Djibouti" : {'Alpha-2': 'DJ', 'Alpha-3': 'DJI', 'Numeric code': '262', 'Link to ISO 3166-2': 'ISO 3166-2:DJ', 'Independent': 'Yes'},
"Dominica" : {'Alpha-2': 'DM', 'Alpha-3': 'DMA', 'Numeric code': '212', 'Link to ISO 3166-2': 'ISO 3166-2:DM', 'Independent': 'Yes'},
"Dominican Republic" : {'Alpha-2': 'DO', 'Alpha-3': 'DOM', 'Numeric code': '214', 'Link to ISO 3166-2': 'ISO 3166-2:DO', 'Independent': 'Yes'},
"Ecuador" : {'Alpha-2': 'EC', 'Alpha-3': 'ECU', 'Numeric code': '218', 'Link to ISO 3166-2': 'ISO 3166-2:EC', 'Independent': 'Yes'},
"Egypt" : {'Alpha-2': 'EG', 'Alpha-3': 'EGY', 'Numeric code': '818', 'Link to ISO 3166-2': 'ISO 3166-2:EG', 'Independent': 'Yes'},
"El Salvador" : {'Alpha-2': 'SV', 'Alpha-3': 'SLV', 'Numeric code': '222', 'Link to ISO 3166-2': 'ISO 3166-2:SV', 'Independent': 'Yes'},
"Equatorial Guinea" : {'Alpha-2': 'GQ', 'Alpha-3': 'GNQ', 'Numeric code': '226', 'Link to ISO 3166-2': 'ISO 3166-2:GQ', 'Independent': 'Yes'},
"Eritrea" : {'Alpha-2': 'ER', 'Alpha-3': 'ERI', 'Numeric code': '232', 'Link to ISO 3166-2': 'ISO 3166-2:ER', 'Independent': 'Yes'},
"Estonia" : {'Alpha-2': 'EE', 'Alpha-3': 'EST', 'Numeric code': '233', 'Link to ISO 3166-2': 'ISO 3166-2:EE', 'Independent': 'Yes'},
"Eswatini" : {'Alpha-2': 'SZ', 'Alpha-3': 'SWZ', 'Numeric code': '748', 'Link to ISO 3166-2': 'ISO 3166-2:SZ', 'Independent': 'Yes'},
"Ethiopia" : {'Alpha-2': 'ET', 'Alpha-3': 'ETH', 'Numeric code': '231', 'Link to ISO 3166-2': 'ISO 3166-2:ET', 'Independent': 'Yes'},
"Falkland Islands (Malvinas)" : {'Alpha-2': 'FK', 'Alpha-3': 'FLK', 'Numeric code': '238', 'Link to ISO 3166-2': 'ISO 3166-2:FK', 'Independent': 'No'},
"Faroe Islands" : {'Alpha-2': 'FO', 'Alpha-3': 'FRO', 'Numeric code': '234', 'Link to ISO 3166-2': 'ISO 3166-2:FO', 'Independent': 'No'},
"Fiji" : {'Alpha-2': 'FJ', 'Alpha-3': 'FJI', 'Numeric code': '242', 'Link to ISO 3166-2': 'ISO 3166-2:FJ', 'Independent': 'Yes'},
"Finland" : {'Alpha-2': 'FI', 'Alpha-3': 'FIN', 'Numeric code': '246', 'Link to ISO 3166-2': 'ISO 3166-2:FI', 'Independent': 'Yes'},
"France" : {'Alpha-2': 'FR', 'Alpha-3': 'FRA', 'Numeric code': '250', 'Link to ISO 3166-2': 'ISO 3166-2:FR', 'Independent': 'Yes'},
"French Guiana" : {'Alpha-2': 'GF', 'Alpha-3': 'GUF', 'Numeric code': '254', 'Link to ISO 3166-2': 'ISO 3166-2:GF', 'Independent': 'No'},
"French Polynesia" : {'Alpha-2': 'PF', 'Alpha-3': 'PYF', 'Numeric code': '258', 'Link to ISO 3166-2': 'ISO 3166-2:PF', 'Independent': 'No'},
"French Southern Territories" : {'Alpha-2': 'TF', 'Alpha-3': 'ATF', 'Numeric code': '260', 'Link to ISO 3166-2': 'ISO 3166-2:TF', 'Independent': 'No'},
"Gabon" : {'Alpha-2': 'GA', 'Alpha-3': 'GAB', 'Numeric code': '266', 'Link to ISO 3166-2': 'ISO 3166-2:GA', 'Independent': 'Yes'},
"Gambia" : {'Alpha-2': 'GM', 'Alpha-3': 'GMB', 'Numeric code': '270', 'Link to ISO 3166-2': 'ISO 3166-2:GM', 'Independent': 'Yes'},
"Georgia" : {'Alpha-2': 'GE', 'Alpha-3': 'GEO', 'Numeric code': '268', 'Link to ISO 3166-2': 'ISO 3166-2:GE', 'Independent': 'Yes'},
"Germany" : {'Alpha-2': 'DE', 'Alpha-3': 'DEU', 'Numeric code': '276', 'Link to ISO 3166-2': 'ISO 3166-2:DE', 'Independent': 'Yes'},
"Ghana" : {'Alpha-2': 'GH', 'Alpha-3': 'GHA', 'Numeric code': '288', 'Link to ISO 3166-2': 'ISO 3166-2:GH', 'Independent': 'Yes'},
"Gibraltar" : {'Alpha-2': 'GI', 'Alpha-3': 'GIB', 'Numeric code': '292', 'Link to ISO 3166-2': 'ISO 3166-2:GI', 'Independent': 'No'},
"Greece" : {'Alpha-2': 'GR', 'Alpha-3': 'GRC', 'Numeric code': '300', 'Link to ISO 3166-2': 'ISO 3166-2:GR', 'Independent': 'Yes'},
"Greenland" : {'Alpha-2': 'GL', 'Alpha-3': 'GRL', 'Numeric code': '304', 'Link to ISO 3166-2': 'ISO 3166-2:GL', 'Independent': 'No'},
"Grenada" : {'Alpha-2': 'GD', 'Alpha-3': 'GRD', 'Numeric code': '308', 'Link to ISO 3166-2': 'ISO 3166-2:GD', 'Independent': 'Yes'},
"Guadeloupe" : {'Alpha-2': 'GP', 'Alpha-3': 'GLP', 'Numeric code': '312', 'Link to ISO 3166-2': 'ISO 3166-2:GP', 'Independent': 'No'},
"Guam" : {'Alpha-2': 'GU', 'Alpha-3': 'GUM', 'Numeric code': '316', 'Link to ISO 3166-2': 'ISO 3166-2:GU', 'Independent': 'No'},
"Guatemala" : {'Alpha-2': 'GT', 'Alpha-3': 'GTM', 'Numeric code': '320', 'Link to ISO 3166-2': 'ISO 3166-2:GT', 'Independent': 'Yes'},
"Guernsey" : {'Alpha-2': 'GG', 'Alpha-3': 'GGY', 'Numeric code': '831', 'Link to ISO 3166-2': 'ISO 3166-2:GG', 'Independent': 'No'},
"Guinea" : {'Alpha-2': 'GN', 'Alpha-3': 'GIN', 'Numeric code': '324', 'Link to ISO 3166-2': 'ISO 3166-2:GN', 'Independent': 'Yes'},
"Guinea-Bissau" : {'Alpha-2': 'GW', 'Alpha-3': 'GNB', 'Numeric code': '624', 'Link to ISO 3166-2': 'ISO 3166-2:GW', 'Independent': 'Yes'},
"Guyana" : {'Alpha-2': 'GY', 'Alpha-3': 'GUY', 'Numeric code': '328', 'Link to ISO 3166-2': 'ISO 3166-2:GY', 'Independent': 'Yes'},
"Haiti" : {'Alpha-2': 'HT', 'Alpha-3': 'HTI', 'Numeric code': '332', 'Link to ISO 3166-2': 'ISO 3166-2:HT', 'Independent': 'Yes'},
"Heard Island and McDonald Islands" : {'Alpha-2': 'HM', 'Alpha-3': 'HMD', 'Numeric code': '334', 'Link to ISO 3166-2': 'ISO 3166-2:HM', 'Independent': 'No'},
"Holy See" : {'Alpha-2': 'VA', 'Alpha-3': 'VAT', 'Numeric code': '336', 'Link to ISO 3166-2': 'ISO 3166-2:VA', 'Independent': 'Yes'},
"Honduras" : {'Alpha-2': 'HN', 'Alpha-3': 'HND', 'Numeric code': '340', 'Link to ISO 3166-2': 'ISO 3166-2:HN', 'Independent': 'Yes'},
"Hong Kong" : {'Alpha-2': 'HK', 'Alpha-3': 'HKG', 'Numeric code': '344', 'Link to ISO 3166-2': 'ISO 3166-2:HK', 'Independent': 'No'},
"Hungary" : {'Alpha-2': 'HU', 'Alpha-3': 'HUN', 'Numeric code': '348', 'Link to ISO 3166-2': 'ISO 3166-2:HU', 'Independent': 'Yes'},
"Iceland" : {'Alpha-2': 'IS', 'Alpha-3': 'ISL', 'Numeric code': '352', 'Link to ISO 3166-2': 'ISO 3166-2:IS', 'Independent': 'Yes'},
"India" : {'Alpha-2': 'IN', 'Alpha-3': 'IND', 'Numeric code': '356', 'Link to ISO 3166-2': 'ISO 3166-2:IN', 'Independent': 'Yes'},
"Indonesia" : {'Alpha-2': 'ID', 'Alpha-3': 'IDN', 'Numeric code': '360', 'Link to ISO 3166-2': 'ISO 3166-2:ID', 'Independent': 'Yes'},
"Iran (Islamic Republic of)" : {'Alpha-2': 'IR', 'Alpha-3': 'IRN', 'Numeric code': '364', 'Link to ISO 3166-2': 'ISO 3166-2:IR', 'Independent': 'Yes'},
"Iraq" : {'Alpha-2': 'IQ', 'Alpha-3': 'IRQ', 'Numeric code': '368', 'Link to ISO 3166-2': 'ISO 3166-2:IQ', 'Independent': 'Yes'},
"Ireland" : {'Alpha-2': 'IE', 'Alpha-3': 'IRL', 'Numeric code': '372', 'Link to ISO 3166-2': 'ISO 3166-2:IE', 'Independent': 'Yes'},
"Isle of Man" : {'Alpha-2': 'IM', 'Alpha-3': 'IMN', 'Numeric code': '833', 'Link to ISO 3166-2': 'ISO 3166-2:IM', 'Independent': 'No'},
"Israel" : {'Alpha-2': 'IL', 'Alpha-3': 'ISR', 'Numeric code': '376', 'Link to ISO 3166-2': 'ISO 3166-2:IL', 'Independent': 'Yes'},
"Italy" : {'Alpha-2': 'IT', 'Alpha-3': 'ITA', 'Numeric code': '380', 'Link to ISO 3166-2': 'ISO 3166-2:IT', 'Independent': 'Yes'},
"Jamaica" : {'Alpha-2': 'JM', 'Alpha-3': 'JAM', 'Numeric code': '388', 'Link to ISO 3166-2': 'ISO 3166-2:JM', 'Independent': 'Yes'},
"Japan" : {'Alpha-2': 'JP', 'Alpha-3': 'JPN', 'Numeric code': '392', 'Link to ISO 3166-2': 'ISO 3166-2:JP', 'Independent': 'Yes'},
"Jersey" : {'Alpha-2': 'JE', 'Alpha-3': 'JEY', 'Numeric code': '832', 'Link to ISO 3166-2': 'ISO 3166-2:JE', 'Independent': 'No'},
"Jordan" : {'Alpha-2': 'JO', 'Alpha-3': 'JOR', 'Numeric code': '400', 'Link to ISO 3166-2': 'ISO 3166-2:JO', 'Independent': 'Yes'},
"Kazakhstan" : {'Alpha-2': 'KZ', 'Alpha-3': 'KAZ', 'Numeric code': '398', 'Link to ISO 3166-2': 'ISO 3166-2:KZ', 'Independent': 'Yes'},
"Kenya" : {'Alpha-2': 'KE', 'Alpha-3': 'KEN', 'Numeric code': '404', 'Link to ISO 3166-2': 'ISO 3166-2:KE', 'Independent': 'Yes'},
"Kiribati" : {'Alpha-2': 'KI', 'Alpha-3': 'KIR', 'Numeric code': '296', 'Link to ISO 3166-2': 'ISO 3166-2:KI', 'Independent': 'Yes'},
"Korea (Democratic People's Republic of)" : {'Alpha-2': 'KP', 'Alpha-3': 'PRK', 'Numeric code': '408', 'Link to ISO 3166-2': 'ISO 3166-2:KP', 'Independent': 'Yes'},
"Korea, Republic of" : {'Alpha-2': 'KR', 'Alpha-3': 'KOR', 'Numeric code': '410', 'Link to ISO 3166-2': 'ISO 3166-2:KR', 'Independent': 'Yes'},
"Kuwait" : {'Alpha-2': 'KW', 'Alpha-3': 'KWT', 'Numeric code': '414', 'Link to ISO 3166-2': 'ISO 3166-2:KW', 'Independent': 'Yes'},
"Kyrgyzstan" : {'Alpha-2': 'KG', 'Alpha-3': 'KGZ', 'Numeric code': '417', 'Link to ISO 3166-2': 'ISO 3166-2:KG', 'Independent': 'Yes'},
"Lao People's Democratic Republic" : {'Alpha-2': 'LA', 'Alpha-3': 'LAO', 'Numeric code': '418', 'Link to ISO 3166-2': 'ISO 3166-2:LA', 'Independent': 'Yes'},
"Latvia" : {'Alpha-2': 'LV', 'Alpha-3': 'LVA', 'Numeric code': '428', 'Link to ISO 3166-2': 'ISO 3166-2:LV', 'Independent': 'Yes'},
"Lebanon" : {'Alpha-2': 'LB', 'Alpha-3': 'LBN', 'Numeric code': '422', 'Link to ISO 3166-2': 'ISO 3166-2:LB', 'Independent': 'Yes'},
"Lesotho" : {'Alpha-2': 'LS', 'Alpha-3': 'LSO', 'Numeric code': '426', 'Link to ISO 3166-2': 'ISO 3166-2:LS', 'Independent': 'Yes'},
"Liberia" : {'Alpha-2': 'LR', 'Alpha-3': 'LBR', 'Numeric code': '430', 'Link to ISO 3166-2': 'ISO 3166-2:LR', 'Independent': 'Yes'},
"Libya" : {'Alpha-2': 'LY', 'Alpha-3': 'LBY', 'Numeric code': '434', 'Link to ISO 3166-2': 'ISO 3166-2:LY', 'Independent': 'Yes'},
"Liechtenstein" : {'Alpha-2': 'LI', 'Alpha-3': 'LIE', 'Numeric code': '438', 'Link to ISO 3166-2': 'ISO 3166-2:LI', 'Independent': 'Yes'},
"Lithuania" : {'Alpha-2': 'LT', 'Alpha-3': 'LTU', 'Numeric code': '440', 'Link to ISO 3166-2': 'ISO 3166-2:LT', 'Independent': 'Yes'},
"Luxembourg" : {'Alpha-2': 'LU', 'Alpha-3': 'LUX', 'Numeric code': '442', 'Link to ISO 3166-2': 'ISO 3166-2:LU', 'Independent': 'Yes'},
"Macao" : {'Alpha-2': 'MO', 'Alpha-3': 'MAC', 'Numeric code': '446', 'Link to ISO 3166-2': 'ISO 3166-2:MO', 'Independent': 'No'},
"Madagascar" : {'Alpha-2': 'MG', 'Alpha-3': 'MDG', 'Numeric code': '450', 'Link to ISO 3166-2': 'ISO 3166-2:MG', 'Independent': 'Yes'},
"Malawi" : {'Alpha-2': 'MW', 'Alpha-3': 'MWI', 'Numeric code': '454', 'Link to ISO 3166-2': 'ISO 3166-2:MW', 'Independent': 'Yes'},
"Malaysia" : {'Alpha-2': 'MY', 'Alpha-3': 'MYS', 'Numeric code': '458', 'Link to ISO 3166-2': 'ISO 3166-2:MY', 'Independent': 'Yes'},
"Maldives" : {'Alpha-2': 'MV', 'Alpha-3': 'MDV', 'Numeric code': '462', 'Link to ISO 3166-2': 'ISO 3166-2:MV', 'Independent': 'Yes'},
"Mali" : {'Alpha-2': 'ML', 'Alpha-3': 'MLI', 'Numeric code': '466', 'Link to ISO 3166-2': 'ISO 3166-2:ML', 'Independent': 'Yes'},
"Malta" : {'Alpha-2': 'MT', 'Alpha-3': 'MLT', 'Numeric code': '470', 'Link to ISO 3166-2': 'ISO 3166-2:MT', 'Independent': 'Yes'},
"Marshall Islands" : {'Alpha-2': 'MH', 'Alpha-3': 'MHL', 'Numeric code': '584', 'Link to ISO 3166-2': 'ISO 3166-2:MH', 'Independent': 'Yes'},
"Martinique" : {'Alpha-2': 'MQ', 'Alpha-3': 'MTQ', 'Numeric code': '474', 'Link to ISO 3166-2': 'ISO 3166-2:MQ', 'Independent': 'No'},
"Mauritania" : {'Alpha-2': 'MR', 'Alpha-3': 'MRT', 'Numeric code': '478', 'Link to ISO 3166-2': 'ISO 3166-2:MR', 'Independent': 'Yes'},
"Mauritius" : {'Alpha-2': 'MU', 'Alpha-3': 'MUS', 'Numeric code': '480', 'Link to ISO 3166-2': 'ISO 3166-2:MU', 'Independent': 'Yes'},
"Mayotte" : {'Alpha-2': 'YT', 'Alpha-3': 'MYT', 'Numeric code': '175', 'Link to ISO 3166-2': 'ISO 3166-2:YT', 'Independent': 'No'},
"Mexico" : {'Alpha-2': 'MX', 'Alpha-3': 'MEX', 'Numeric code': '484', 'Link to ISO 3166-2': 'ISO 3166-2:MX', 'Independent': 'Yes'},
"Micronesia (Federated States of)" : {'Alpha-2': 'FM', 'Alpha-3': 'FSM', 'Numeric code': '583', 'Link to ISO 3166-2': 'ISO 3166-2:FM', 'Independent': 'Yes'},
"Moldova, Republic of" : {'Alpha-2': 'MD', 'Alpha-3': 'MDA', 'Numeric code': '498', 'Link to ISO 3166-2': 'ISO 3166-2:MD', 'Independent': 'Yes'},
"Monaco" : {'Alpha-2': 'MC', 'Alpha-3': 'MCO', 'Numeric code': '492', 'Link to ISO 3166-2': 'ISO 3166-2:MC', 'Independent': 'Yes'},
"Mongolia" : {'Alpha-2': 'MN', 'Alpha-3': 'MNG', 'Numeric code': '496', 'Link to ISO 3166-2': 'ISO 3166-2:MN', 'Independent': 'Yes'},
"Montenegro" : {'Alpha-2': 'ME', 'Alpha-3': 'MNE', 'Numeric code': '499', 'Link to ISO 3166-2': 'ISO 3166-2:ME', 'Independent': 'Yes'},
"Montserrat" : {'Alpha-2': 'MS', 'Alpha-3': 'MSR', 'Numeric code': '500', 'Link to ISO 3166-2': 'ISO 3166-2:MS', 'Independent': 'No'},
"Morocco" : {'Alpha-2': 'MA', 'Alpha-3': 'MAR', 'Numeric code': '504', 'Link to ISO 3166-2': 'ISO 3166-2:MA', 'Independent': 'Yes'},
"Mozambique" : {'Alpha-2': 'MZ', 'Alpha-3': 'MOZ', 'Numeric code': '508', 'Link to ISO 3166-2': 'ISO 3166-2:MZ', 'Independent': 'Yes'},
"Myanmar" : {'Alpha-2': 'MM', 'Alpha-3': 'MMR', 'Numeric code': '104', 'Link to ISO 3166-2': 'ISO 3166-2:MM', 'Independent': 'Yes'},
"Namibia" : {'Alpha-2': 'NA', 'Alpha-3': 'NAM', 'Numeric code': '516', 'Link to ISO 3166-2': 'ISO 3166-2:NA', 'Independent': 'Yes'},
"Nauru" : {'Alpha-2': 'NR', 'Alpha-3': 'NRU', 'Numeric code': '520', 'Link to ISO 3166-2': 'ISO 3166-2:NR', 'Independent': 'Yes'},
"Nepal" : {'Alpha-2': 'NP', 'Alpha-3': 'NPL', 'Numeric code': '524', 'Link to ISO 3166-2': 'ISO 3166-2:NP', 'Independent': 'Yes'},
"Netherlands" : {'Alpha-2': 'NL', 'Alpha-3': 'NLD', 'Numeric code': '528', 'Link to ISO 3166-2': 'ISO 3166-2:NL', 'Independent': 'Yes'},
"New Caledonia" : {'Alpha-2': 'NC', 'Alpha-3': 'NCL', 'Numeric code': '540', 'Link to ISO 3166-2': 'ISO 3166-2:NC', 'Independent': 'No'},
"New Zealand" : {'Alpha-2': 'NZ', 'Alpha-3': 'NZL', 'Numeric code': '554', 'Link to ISO 3166-2': 'ISO 3166-2:NZ', 'Independent': 'Yes'},
"Nicaragua" : {'Alpha-2': 'NI', 'Alpha-3': 'NIC', 'Numeric code': '558', 'Link to ISO 3166-2': 'ISO 3166-2:NI', 'Independent': 'Yes'},
"Niger" : {'Alpha-2': 'NE', 'Alpha-3': 'NER', 'Numeric code': '562', 'Link to ISO 3166-2': 'ISO 3166-2:NE', 'Independent': 'Yes'},
"Nigeria" : {'Alpha-2': 'NG', 'Alpha-3': 'NGA', 'Numeric code': '566', 'Link to ISO 3166-2': 'ISO 3166-2:NG', 'Independent': 'Yes'},
"Niue" : {'Alpha-2': 'NU', 'Alpha-3': 'NIU', 'Numeric code': '570', 'Link to ISO 3166-2': 'ISO 3166-2:NU', 'Independent': 'No'},
"Norfolk Island" : {'Alpha-2': 'NF', 'Alpha-3': 'NFK', 'Numeric code': '574', 'Link to ISO 3166-2': 'ISO 3166-2:NF', 'Independent': 'No'},
"North Macedonia" : {'Alpha-2': 'MK', 'Alpha-3': 'MKD', 'Numeric code': '807', 'Link to ISO 3166-2': 'ISO 3166-2:MK', 'Independent': 'Yes'},
"Northern Mariana Islands" : {'Alpha-2': 'MP', 'Alpha-3': 'MNP', 'Numeric code': '580', 'Link to ISO 3166-2': 'ISO 3166-2:MP', 'Independent': 'No'},
"Norway" : {'Alpha-2': 'NO', 'Alpha-3': 'NOR', 'Numeric code': '578', 'Link to ISO 3166-2': 'ISO 3166-2:NO', 'Independent': 'Yes'},
"Oman" : {'Alpha-2': 'OM', 'Alpha-3': 'OMN', 'Numeric code': '512', 'Link to ISO 3166-2': 'ISO 3166-2:OM', 'Independent': 'Yes'},
"Pakistan" : {'Alpha-2': 'PK', 'Alpha-3': 'PAK', 'Numeric code': '586', 'Link to ISO 3166-2': 'ISO 3166-2:PK', 'Independent': 'Yes'},
"Palau" : {'Alpha-2': 'PW', 'Alpha-3': 'PLW', 'Numeric code': '585', 'Link to ISO 3166-2': 'ISO 3166-2:PW', 'Independent': 'Yes'},
"Palestine, State of" : {'Alpha-2': 'PS', 'Alpha-3': 'PSE', 'Numeric code': '275', 'Link to ISO 3166-2': 'ISO 3166-2:PS', 'Independent': 'No'},
"Panama" : {'Alpha-2': 'PA', 'Alpha-3': 'PAN', 'Numeric code': '591', 'Link to ISO 3166-2': 'ISO 3166-2:PA', 'Independent': 'Yes'},
"Papua New Guinea" : {'Alpha-2': 'PG', 'Alpha-3': 'PNG', 'Numeric code': '598', 'Link to ISO 3166-2': 'ISO 3166-2:PG', 'Independent': 'Yes'},
"Paraguay" : {'Alpha-2': 'PY', 'Alpha-3': 'PRY', 'Numeric code': '600', 'Link to ISO 3166-2': 'ISO 3166-2:PY', 'Independent': 'Yes'},
"Peru" : {'Alpha-2': 'PE', 'Alpha-3': 'PER', 'Numeric code': '604', 'Link to ISO 3166-2': 'ISO 3166-2:PE', 'Independent': 'Yes'},
"Philippines" : {'Alpha-2': 'PH', 'Alpha-3': 'PHL', 'Numeric code': '608', 'Link to ISO 3166-2': 'ISO 3166-2:PH', 'Independent': 'Yes'},
"Pitcairn" : {'Alpha-2': 'PN', 'Alpha-3': 'PCN', 'Numeric code': '612', 'Link to ISO 3166-2': 'ISO 3166-2:PN', 'Independent': 'No'},
"Poland" : {'Alpha-2': 'PL', 'Alpha-3': 'POL', 'Numeric code': '616', 'Link to ISO 3166-2': 'ISO 3166-2:PL', 'Independent': 'Yes'},
"Portugal" : {'Alpha-2': 'PT', 'Alpha-3': 'PRT', 'Numeric code': '620', 'Link to ISO 3166-2': 'ISO 3166-2:PT', 'Independent': 'Yes'},
"Puerto Rico" : {'Alpha-2': 'PR', 'Alpha-3': 'PRI', 'Numeric code': '630', 'Link to ISO 3166-2': 'ISO 3166-2:PR', 'Independent': 'No'},
"Qatar" : {'Alpha-2': 'QA', 'Alpha-3': 'QAT', 'Numeric code': '634', 'Link to ISO 3166-2': 'ISO 3166-2:QA', 'Independent': 'Yes'},
"Réunion" : {'Alpha-2': 'RE', 'Alpha-3': 'REU', 'Numeric code': '638', 'Link to ISO 3166-2': 'ISO 3166-2:RE', 'Independent': 'No'},
"Romania" : {'Alpha-2': 'RO', 'Alpha-3': 'ROU', 'Numeric code': '642', 'Link to ISO 3166-2': 'ISO 3166-2:RO', 'Independent': 'Yes'},
"Russian Federation" : {'Alpha-2': 'RU', 'Alpha-3': 'RUS', 'Numeric code': '643', 'Link to ISO 3166-2': 'ISO 3166-2:RU', 'Independent': 'Yes'},
"Rwanda" : {'Alpha-2': 'RW', 'Alpha-3': 'RWA', 'Numeric code': '646', 'Link to ISO 3166-2': 'ISO 3166-2:RW', 'Independent': 'Yes'},
"Saint Barthélemy" : {'Alpha-2': 'BL', 'Alpha-3': 'BLM', 'Numeric code': '652', 'Link to ISO 3166-2': 'ISO 3166-2:BL', 'Independent': 'No'},
"Saint Helena, Ascension and Tristan da Cunha" : {'Alpha-2': 'SH', 'Alpha-3': 'SHN', 'Numeric code': '654', 'Link to ISO 3166-2': 'ISO 3166-2:SH', 'Independent': 'No'},
"Saint Kitts and Nevis" : {'Alpha-2': 'KN', 'Alpha-3': 'KNA', 'Numeric code': '659', 'Link to ISO 3166-2': 'ISO 3166-2:KN', 'Independent': 'Yes'},
"Saint Lucia" : {'Alpha-2': 'LC', 'Alpha-3': 'LCA', 'Numeric code': '662', 'Link to ISO 3166-2': 'ISO 3166-2:LC', 'Independent': 'Yes'},
"Saint Martin (French part)" : {'Alpha-2': 'MF', 'Alpha-3': 'MAF', 'Numeric code': '663', 'Link to ISO 3166-2': 'ISO 3166-2:MF', 'Independent': 'No'},
"Saint Pierre and Miquelon" : {'Alpha-2': 'PM', 'Alpha-3': 'SPM', 'Numeric code': '666', 'Link to ISO 3166-2': 'ISO 3166-2:PM', 'Independent': 'No'},
"Saint Vincent and the Grenadines" : {'Alpha-2': 'VC', 'Alpha-3': 'VCT', 'Numeric code': '670', 'Link to ISO 3166-2': 'ISO 3166-2:VC', 'Independent': 'Yes'},
"Samoa" : {'Alpha-2': 'WS', 'Alpha-3': 'WSM', 'Numeric code': '882', 'Link to ISO 3166-2': 'ISO 3166-2:WS', 'Independent': 'Yes'},
"San Marino" : {'Alpha-2': 'SM', 'Alpha-3': 'SMR', 'Numeric code': '674', 'Link to ISO 3166-2': 'ISO 3166-2:SM', 'Independent': 'Yes'},
"Sao Tome and Principe" : {'Alpha-2': 'ST', 'Alpha-3': 'STP', 'Numeric code': '678', 'Link to ISO 3166-2': 'ISO 3166-2:ST', 'Independent': 'Yes'},
"Saudi Arabia" : {'Alpha-2': 'SA', 'Alpha-3': 'SAU', 'Numeric code': '682', 'Link to ISO 3166-2': 'ISO 3166-2:SA', 'Independent': 'Yes'},
"Senegal" : {'Alpha-2': 'SN', 'Alpha-3': 'SEN', 'Numeric code': '686', 'Link to ISO 3166-2': 'ISO 3166-2:SN', 'Independent': 'Yes'},
"Serbia" : {'Alpha-2': 'RS', 'Alpha-3': 'SRB', 'Numeric code': '688', 'Link to ISO 3166-2': 'ISO 3166-2:RS', 'Independent': 'Yes'},
"Seychelles" : {'Alpha-2': 'SC', 'Alpha-3': 'SYC', 'Numeric code': '690', 'Link to ISO 3166-2': 'ISO 3166-2:SC', 'Independent': 'Yes'},
"Sierra Leone" : {'Alpha-2': 'SL', 'Alpha-3': 'SLE', 'Numeric code': '694', 'Link to ISO 3166-2': 'ISO 3166-2:SL', 'Independent': 'Yes'},
"Singapore" : {'Alpha-2': 'SG', 'Alpha-3': 'SGP', 'Numeric code': '702', 'Link to ISO 3166-2': 'ISO 3166-2:SG', 'Independent': 'Yes'},
"Sint Maarten (Dutch part)" : {'Alpha-2': 'SX', 'Alpha-3': 'SXM', 'Numeric code': '534', 'Link to ISO 3166-2': 'ISO 3166-2:SX', 'Independent': 'No'},
"Slovakia" : {'Alpha-2': 'SK', 'Alpha-3': 'SVK', 'Numeric code': '703', 'Link to ISO 3166-2': 'ISO 3166-2:SK', 'Independent': 'Yes'},
"Slovenia" : {'Alpha-2': 'SI', 'Alpha-3': 'SVN', 'Numeric code': '705', 'Link to ISO 3166-2': 'ISO 3166-2:SI', 'Independent': 'Yes'},
"Solomon Islands" : {'Alpha-2': 'SB', 'Alpha-3': 'SLB', 'Numeric code': '090', 'Link to ISO 3166-2': 'ISO 3166-2:SB', 'Independent': 'Yes'},
"Somalia" : {'Alpha-2': 'SO', 'Alpha-3': 'SOM', 'Numeric code': '706', 'Link to ISO 3166-2': 'ISO 3166-2:SO', 'Independent': 'Yes'},
"South Africa" : {'Alpha-2': 'ZA', 'Alpha-3': 'ZAF', 'Numeric code': '710', 'Link to ISO 3166-2': 'ISO 3166-2:ZA', 'Independent': 'Yes'},
"South Georgia and the South Sandwich Islands" : {'Alpha-2': 'GS', 'Alpha-3': 'SGS', 'Numeric code': '239', 'Link to ISO 3166-2': 'ISO 3166-2:GS', 'Independent': 'No'},
"South Sudan" : {'Alpha-2': 'SS', 'Alpha-3': 'SSD', 'Numeric code': '728', 'Link to ISO 3166-2': 'ISO 3166-2:SS', 'Independent': 'Yes'},
"Spain" : {'Alpha-2': 'ES', 'Alpha-3': 'ESP', 'Numeric code': '724', 'Link to ISO 3166-2': 'ISO 3166-2:ES', 'Independent': 'Yes'},
"Sri Lanka" : {'Alpha-2': 'LK', 'Alpha-3': 'LKA', 'Numeric code': '144', 'Link to ISO 3166-2': 'ISO 3166-2:LK', 'Independent': 'Yes'},
"Sudan" : {'Alpha-2': 'SD', 'Alpha-3': 'SDN', 'Numeric code': '729', 'Link to ISO 3166-2': 'ISO 3166-2:SD', 'Independent': 'Yes'},
"Suriname" : {'Alpha-2': 'SR', 'Alpha-3': 'SUR', 'Numeric code': '740', 'Link to ISO 3166-2': 'ISO 3166-2:SR', 'Independent': 'Yes'},
"Svalbard and Jan Mayen" : {'Alpha-2': 'SJ', 'Alpha-3': 'SJM', 'Numeric code': '744', 'Link to ISO 3166-2': 'ISO 3166-2:SJ', 'Independent': 'No'},
"Sweden" : {'Alpha-2': 'SE', 'Alpha-3': 'SWE', 'Numeric code': '752', 'Link to ISO 3166-2': 'ISO 3166-2:SE', 'Independent': 'Yes'},
"Switzerland" : {'Alpha-2': 'CH', 'Alpha-3': 'CHE', 'Numeric code': '756', 'Link to ISO 3166-2': 'ISO 3166-2:CH', 'Independent': 'Yes'},
"Syrian Arab Republic" : {'Alpha-2': 'SY', 'Alpha-3': 'SYR', 'Numeric code': '760', 'Link to ISO 3166-2': 'ISO 3166-2:SY', 'Independent': 'Yes'},
"Taiwan" : {'Alpha-2': 'TW', 'Alpha-3': 'TWN', 'Numeric code': '158', 'Link to ISO 3166-2': 'ISO 3166-2:TW', 'Independent': 'No'},
"Tajikistan" : {'Alpha-2': 'TJ', 'Alpha-3': 'TJK', 'Numeric code': '762', 'Link to ISO 3166-2': 'ISO 3166-2:TJ', 'Independent': 'Yes'},
"Tanzania, United Republic of" : {'Alpha-2': 'TZ', 'Alpha-3': 'TZA', 'Numeric code': '834', 'Link to ISO 3166-2': 'ISO 3166-2:TZ', 'Independent': 'Yes'},
"Thailand" : {'Alpha-2': 'TH', 'Alpha-3': 'THA', 'Numeric code': '764', 'Link to ISO 3166-2': 'ISO 3166-2:TH', 'Independent': 'Yes'},
"Timor-Leste" : {'Alpha-2': 'TL', 'Alpha-3': 'TLS', 'Numeric code': '626', 'Link to ISO 3166-2': 'ISO 3166-2:TL', 'Independent': 'Yes'},
"Togo" : {'Alpha-2': 'TG', 'Alpha-3': 'TGO', 'Numeric code': '768', 'Link to ISO 3166-2': 'ISO 3166-2:TG', 'Independent': 'Yes'},
"Tokelau" : {'Alpha-2': 'TK', 'Alpha-3': 'TKL', 'Numeric code': '772', 'Link to ISO 3166-2': 'ISO 3166-2:TK', 'Independent': 'No'},
"Tonga" : {'Alpha-2': 'TO', 'Alpha-3': 'TON', 'Numeric code': '776', 'Link to ISO 3166-2': 'ISO 3166-2:TO', 'Independent': 'Yes'},
"Trinidad and Tobago" : {'Alpha-2': 'TT', 'Alpha-3': 'TTO', 'Numeric code': '780', 'Link to ISO 3166-2': 'ISO 3166-2:TT', 'Independent': 'Yes'},
"Tunisia" : {'Alpha-2': 'TN', 'Alpha-3': 'TUN', 'Numeric code': '788', 'Link to ISO 3166-2': 'ISO 3166-2:TN', 'Independent': 'Yes'},
"Turkey" : {'Alpha-2': 'TR', 'Alpha-3': 'TUR', 'Numeric code': '792', 'Link to ISO 3166-2': 'ISO 3166-2:TR', 'Independent': 'Yes'},
"Turkmenistan" : {'Alpha-2': 'TM', 'Alpha-3': 'TKM', 'Numeric code': '795', 'Link to ISO 3166-2': 'ISO 3166-2:TM', 'Independent': 'Yes'},
"Turks and Caicos Islands" : {'Alpha-2': 'TC', 'Alpha-3': 'TCA', 'Numeric code': '796', 'Link to ISO 3166-2': 'ISO 3166-2:TC', 'Independent': 'No'},
"Tuvalu" : {'Alpha-2': 'TV', 'Alpha-3': 'TUV', 'Numeric code': '798', 'Link to ISO 3166-2': 'ISO 3166-2:TV', 'Independent': 'Yes'},
"Uganda" : {'Alpha-2': 'UG', 'Alpha-3': 'UGA', 'Numeric code': '800', 'Link to ISO 3166-2': 'ISO 3166-2:UG', 'Independent': 'Yes'},
"Ukraine" : {'Alpha-2': 'UA', 'Alpha-3': 'UKR', 'Numeric code': '804', 'Link to ISO 3166-2': 'ISO 3166-2:UA', 'Independent': 'Yes'},
"United Arab Emirates" : {'Alpha-2': 'AE', 'Alpha-3': 'ARE', 'Numeric code': '784', 'Link to ISO 3166-2': 'ISO 3166-2:AE', 'Independent': 'Yes'},
"United Kingdom of Great Britain and Northern Ireland" : {'Alpha-2': 'GB', 'Alpha-3': 'GBR', 'Numeric code': '826', 'Link to ISO 3166-2': 'ISO 3166-2:GB', 'Independent': 'Yes'},
"United States of America" : {'Alpha-2': 'US', 'Alpha-3': 'USA', 'Numeric code': '840', 'Link to ISO 3166-2': 'ISO 3166-2:US', 'Independent': 'Yes'},
"United States Minor Outlying Islands" : {'Alpha-2': 'UM', 'Alpha-3': 'UMI', 'Numeric code': '581', 'Link to ISO 3166-2': 'ISO 3166-2:UM', 'Independent': 'No'},
"Uruguay" : {'Alpha-2': 'UY', 'Alpha-3': 'URY', 'Numeric code': '858', 'Link to ISO 3166-2': 'ISO 3166-2:UY', 'Independent': 'Yes'},
"Uzbekistan" : {'Alpha-2': 'UZ', 'Alpha-3': 'UZB', 'Numeric code': '860', 'Link to ISO 3166-2': 'ISO 3166-2:UZ', 'Independent': 'Yes'},
"Vanuatu" : {'Alpha-2': 'VU', 'Alpha-3': 'VUT', 'Numeric code': '548', 'Link to ISO 3166-2': 'ISO 3166-2:VU', 'Independent': 'Yes'},
"Venezuela (Bolivarian Republic of)" : {'Alpha-2': 'VE', 'Alpha-3': 'VEN', 'Numeric code': '862', 'Link to ISO 3166-2': 'ISO 3166-2:VE', 'Independent': 'Yes'},
"Viet Nam" : {'Alpha-2': 'VN', 'Alpha-3': 'VNM', 'Numeric code': '704', 'Link to ISO 3166-2': 'ISO 3166-2:VN', 'Independent': 'Yes'},
"Virgin Islands (British)" : {'Alpha-2': 'VG', 'Alpha-3': 'VGB', 'Numeric code': '092', 'Link to ISO 3166-2': 'ISO 3166-2:VG', 'Independent': 'No'},
"Virgin Islands (U.S.)" : {'Alpha-2': 'VI', 'Alpha-3': 'VIR', 'Numeric code': '850', 'Link to ISO 3166-2': 'ISO 3166-2:VI', 'Independent': 'No'},
"Wallis and Futuna" : {'Alpha-2': 'WF', 'Alpha-3': 'WLF', 'Numeric code': '876', 'Link to ISO 3166-2': 'ISO 3166-2:WF', 'Independent': 'No'},
"Western Sahara" : {'Alpha-2': 'EH', 'Alpha-3': 'ESH', 'Numeric code': '732', 'Link to ISO 3166-2': 'ISO 3166-2:EH', 'Independent': 'No'},
"Yemen" : {'Alpha-2': 'YE', 'Alpha-3': 'YEM', 'Numeric code': '887', 'Link to ISO 3166-2': 'ISO 3166-2:YE', 'Independent': 'Yes'},
"Zambia" : {'Alpha-2': 'ZM', 'Alpha-3': 'ZMB', 'Numeric code': '894', 'Link to ISO 3166-2': 'ISO 3166-2:ZM', 'Independent': 'Yes'},
"Zimbabwe" : {'Alpha-2': 'ZW', 'Alpha-3': 'ZWE', 'Numeric code': '716', 'Link to ISO 3166-2': 'ISO 3166-2:ZW', 'Independent': 'Yes'} }



# numb_pages - Number of pages for the corresponding year 1982-2019, 38 years in total
numb_pages = [520,	646,	856,	643,	715,	923,	1359,	1375,	1779,	1646,	1410,	1396,	1679,	1566,	2106,	2067,	2092,	2061,	2484,	2135,	2478,	2452,	2586,	2668,	3541,	3124,	3713,	4338,	4453,	4424,	4609,	5258,	5183,	5634,	5654,	6093,	5520, 5407]
numb_symbols_SEG = [3876563, 4300006, 5583145, 4577432, 4441406, 3181421, 4917848, 5030196, 6127287, 5740092, 5058741, 4768892, 6214099, 5583137, 6871658, 6897945, 7437265, 6917126, 8870421, 7731253, 9153100, 9268921, 9589137, 11012435, 11672829, 10477110, 11908644, 14437507, 14950656, 14756723, 15764247, 18001005, 17897258, 19463649, 20051753, 21314341, 19912746, 20069435]


aver_coauth_numb_SEG = [2.1589403973509933, 2.1052631578947367, 1.9828009828009827, 2.2161383285302594, 2.058219178082192, 2.148014440433213, 2.1649484536082473, 2.313131313131313, 2.3133462282398454, 2.2195121951219514, 2.2872062663185377, 2.355, 2.504291845493562, 2.6057906458797326, 2.6205128205128205, 2.669741697416974, 2.734061930783242, 2.837638376383764, 2.908805031446541, 2.8248175182481754, 2.9011164274322168, 3.103448275862069, 3.0693815987933637, 3.127565982404692, 3.1204481792717087, 3.126782884310618, 3.3454790823211877, 3.2354948805460753, 3.308132875143184, 3.44815668202765, 3.552836484983315, 3.433628318584071, 3.494959677419355, 3.571296296296296, 3.476449275362319, 3.6575342465753424, 3.6621743036837375, 3.9009259259259259259259259259259]
aver_coauth_numb_EAGE = [3.05, 3.0676258992805754, 2.979466119096509, 3.1364341085271317, 3.152269399707174, 3.044776119402985, 3.117283950617284, 3.2708978328173375, 3.2417127071823204, 3.3980044345898004, 3.1833872707659117, 3.227355072463768, 3.4643714971977584, 3.646404109589041, 3.7708333333333335, 3.671511627906977, 3.599670510708402, 3.6703577512776833, 3.9076923076923076]
aver_coauth_numb_SPE = [2.59, 2.488722, 2.708333, 2.827869, 2.654321, 3.18595, 3.170455, 0.001, 3.263975, 3.194986, 3.360606, 3.29661, 3.431635, 3.392111, 3.491111, 3.400458, 3.588358, 3.596401, 3.609694, 3.392105, 3.812933, 3.648718, 4.010929, 3.709596, 3.740437, 3.869452, 4.221662, 4.067708, 4.17757, 4.352304]

ref_data = [2.285361,2.269854,2.285205,2.274893, 2.32184, 2.352931, 2.433209, 2.402235, 2.433422, 2.49702, 2.594231, 2.581554, 2.727233, 2.789873, 2.874077, 2.885946, 3.018021, 3.166208, 3.372227, 3.288681, 3.346355, 3.463061, 3.437281, 3.519684, 3.67232, 3.747994, 3.896395, 3.848252, 4.055962, 4.122729, 4.207524, 4.246959, 4.315808, 4.348695, 4.480921, 4.601956, 4.730707]

aver_pages_SEG = [i / 3000 for i in numb_symbols_SEG]
# numb_symbols_EAGE - Number of symbols for each of the corresponding year 2001-2019, 19 years in total
numb_symbols_EAGE = [5504576, 6691125, 5001435, 6697122, 9786123, 5271969, 6992646, 7889951, 8179235, 11006371, 10703326, 15831187, 16963000, 13753199, 13615665, 13641114, 15426915, 14449214, 12885065]
aver_pages_EAGE = [ i / 3000 for i in numb_symbols_EAGE]
# numb_papers - Number of articles for the corresponding year 1982-2019, 38 years in total
numb_articles = [302,	323,	407,	347,	292,	277,	388,	396,	517,	451,	383,	400,	466,	449,	585,	542,	549,	542,	636,	548,	627,	638,	663,	682,	714,	631,	741,	879,	873,	868,	899,	1017,	992,	1080,	1104,	1168,	1113, 1080]
# The price of oil from 1980 to 2019
oil_price = [37.42, 35.75, 32.38,	29.04,	28.2,	27.01,	13.53,	17.73,	14.24,	17.31,	22.26,	18.62,	18.44,	16.33,	15.53,	16.86,	20.29,	18.86,	12.28,	17.44,	27.6,	23.12,	24.36,	28.1,	36.05,	50.59,	61,	69.04,	94.1,	60.86,	77.38,	107.46,	109.45,	105.87,	96.29,	49.49,	40.76,	52.51,	69.78, 63.83]
# https://inflationdata.com/articles/inflation-adjusted-prices/historical-crude-oil-prices-table/
# The price of oil from 1979 to 2020 (first three months of 2020) taking into account the inflation
oil_price_infl = [88.38, 117.3, 101.57, 85.15, 75.34, 71.41, 64.56, 33.97, 40.3, 32.48, 38.13, 45.65, 38.26, 35.39, 29.92, 27.25, 28.36, 33.63, 29.96, 18.86, 25.58, 41.02, 33.52, 32.69, 38.84, 51.39, 66.04, 74.59, 79.73, 109.25, 64.19, 84.24, 99.83, 97.17, 100.95, 93.24, 45.55, 39.02, 43.97, 57.77, 50.01, 39.42]
# ExxonMObil stock market price https://finance.yahoo.com/quote/XOM/history?period1=-252374400&period2=1588464000&interval=1mo&filter=history&frequency=1mo
# January 1, 1962 - May 1, 2020. Monthly closeing price 
# 1990 - 2019 window equal to 348
exxon_stock_pr = [43.14, 46.47, 37.97, 51.44, 62.12, 69.78, 68.13, 67.57, 70.61, 68.48, 74.36, 76.63, 70.77, 80.28, 80.8, 79.03, 73.28, 68.19, 79.5, 79.68, 85.02, 80.17, 81.51, 82.73, 81.24, 77.75, 74.61, 75.74, 87.3, 83.64, 83.29, 83.35, 81.98, 76.33, 80.04, 80.73, 80.5, 81.65, 82.01, 81.32, 83.89, 90.26, 87.3, 83.32, 87.28, 87.14, 88.95, 93.74, 89.02, 88.4, 83.59, 80.15, 77.85, 77.95, 81.66, 82.74, 74.35, 75.24, 79.21, 83.2, 85.2, 87.37, 85, 88.54, 87.42, 92.45, 90.54, 96.71, 94.05, 99.46, 98.94, 100.68, 100.53, 102.41, 97.68, 96.27, 92.16, 101.2, 93.48, 89.62, 86.04, 87.16, 93.75, 90.35, 90.47, 88.99, 90.11, 89.55, 89.97, 86.55, 88.14, 91.17, 91.45, 87.3, 86.85, 85.57, 78.63, 86.34, 86.73, 86.5, 83.74, 84.76, 80.44, 78.09, 72.63, 74.02, 79.79, 81.38, 83.47, 87.98, 84.13, 85.53, 80.68, 73.12, 69.56, 66.49, 61.79, 59.11, 59.68, 57.07, 60.46, 67.77, 66.98, 65, 64.43, 68.19, 75.07, 71.67, 68.61, 69.15, 70.39, 69.91, 69.35, 66.67, 68.1, 67.9, 76.48, 79.83, 80.15, 74.12, 77.66, 80.01, 80.43, 88.13, 88.76, 93.07, 84.58, 87.01, 85.7, 93.69, 89.16, 91.99, 92.56, 85.73, 85.13, 83.88, 83.17, 79.38, 75.45, 71.68, 74.1, 76.63, 76.81, 71.42, 67.1, 67.67, 67.74, 61.35, 60.91, 63.08, 60.86, 59.37, 62.75, 56.17, 58.03, 56.14, 63.54, 59.9, 58.75, 57.47, 56.2, 57.03, 59.6, 63.31, 51.6, 51.26, 51.25, 49.22, 48.33, 46.1, 46.3, 44.41, 43.25, 42.55, 41.59, 42.17, 40.79, 41, 36.2, 36.58, 36.6, 37.7, 35.58, 35.91, 36.4, 35.2, 34.95, 34.02, 34.15, 34.94, 34.8, 33.66, 31.9, 35.45, 36.76, 40.92, 39.93, 40.17, 43.83, 41.3, 39.05, 39.3, 37.4, 39.45, 39.4, 40.15, 41.76, 43.67, 44.38, 44.3, 40.5, 40.53, 42.08, 43.47, 44, 44.59, 44.55, 40.82, 40.09, 39.25, 41.66, 38.84, 39, 37.66, 41.44, 40.28, 39.66, 37.03, 38, 39.44, 39.69, 38.56, 39.94, 41.53, 35.28, 33.28, 35.13, 36.56, 37.5, 35.81, 35.31, 32.72, 35.13, 35.69, 35.25, 36.53, 33.81, 31.88, 29.66, 30.59, 30.5, 30.72, 32.03, 30.59, 32.13, 30.63, 29.63, 28.31, 26.94, 25.06, 25.91, 24.5, 23.59, 22.16, 20.81, 20.38, 20.56, 21.72, 21.19, 21.25, 20.38, 19.88, 20.06, 20.28, 19.34, 19.09, 18.06, 17.19, 18.13, 17.66, 17.84, 17.38, 16.66, 15.97, 15.63, 15.19, 15.09, 15.72, 14.38, 14.88, 14.88, 14.19, 15.28, 15.72, 15.72, 16.22, 16.63, 15.78, 15.69, 16.34, 16.38, 16.34, 16.41, 16.53, 16.38, 16.5, 16.53, 15.91, 15.28, 15.28, 14.88, 15.31, 15.97, 16.06, 15.88, 15.47, 15.16, 15, 13.69, 14.28, 14.56, 15.22, 14.66, 15.25, 14.88, 14.56, 14.84, 14.53, 14.56, 14.88, 14.63, 13.78, 12.91, 12.94, 12.66, 12.25, 12.25, 12.5, 12.97, 11.97, 12, 11.31, 11.56, 11.75, 11.75, 12.5, 11.81, 11.5, 11.19, 10.94, 11.44, 11, 10.78, 10.78, 10.97, 10.97, 11.59, 11, 10.81, 11.19, 11.19, 11.63, 11.84, 11.34, 11.25, 11.22, 10.5, 10.66, 10.5, 9.53, 9.19, 10.66, 12.16, 12.45, 11.77, 11.66, 10.88, 10.83, 10.72, 9.8, 10.34, 8.77, 8.66, 8.5, 8.41, 8.61, 7.59, 7.61, 7.48, 7.08, 6.97, 6.53, 6.47, 6.89, 6.67, 6.88, 6.48, 6.59, 6.56, 6.73, 6.75, 6.44, 6.28, 5.94, 6, 5.63, 5.41, 5.47, 5.59, 5.38, 4.8, 5.11, 4.98, 5.33, 4.83, 4.81, 4.97, 4.67, 4.72, 4.78, 4.56, 4.75, 4.48, 4.22, 4.22, 4.42, 3.86, 3.66, 3.77, 3.72, 3.5, 3.7, 3.5, 3.56, 3.25, 3.47, 3.5, 3.53, 3.52, 3.59, 3.83, 3.91, 4.09, 3.8, 3.89, 4.06, 4.36, 4.28, 4.05, 4.28, 4.29, 4.5, 4.86, 5.04, 5.49, 4.76, 4.36, 4.38, 4.35, 4.14, 4, 3.8, 3.62, 4.09, 3.8, 3.45, 3.63, 3.59, 3.69, 3.51, 3.42, 3.37, 3.11, 3.32, 3.3, 3.08, 3.2, 3.07, 3.07, 3, 3.24, 3.09, 2.91, 2.74, 2.92, 2.95, 2.79, 2.75, 2.86, 3.01, 2.91, 2.95, 3.02, 3.03, 3.23, 3.34, 3.2, 3.23, 3.17, 3.18, 3.34, 3.35, 3.2, 3.28, 3.47, 3.3, 3.32, 3.27, 3.15, 2.95, 2.93, 2.72, 2.84, 2.77, 2.69, 2.79, 2.73, 2.71, 2.72, 2.89, 2.74, 2.53, 2.31, 2.42, 2.29, 2.02, 1.96, 2.14, 1.84, 2.1, 2.34, 2.19, 2.27, 2.41, 2.54, 2.61, 2.7, 2.94, 2.8, 2.95, 2.9, 2.78, 2.99, 3.08, 2.93, 3.01, 2.95, 2.79, 2.96, 2.73, 2.73, 2.61, 2.54, 2.54, 2.37, 2.32, 2.35, 2.18, 2.2, 2.36, 2.35, 2.3, 2.15, 2.19, 2.25, 2.21, 2.39, 2.36, 2.37, 2.49, 2.49, 2.35, 2.21, 2.29, 2.26, 2.17, 2.09, 2.06, 1.94, 1.71, 1.77, 1.68, 1.79, 1.69, 1.76, 1.93, 1.94, 2.09, 2.15, 2.28, 2.18, 2.43, 2.62, 2.53, 2.57, 2.43, 2.5, 2.46, 2.65, 2.53, 2.43, 2.46, 2.45, 2.13, 2.11, 2.24, 2.18, 2.12, 2.16, 2.11, 2.08, 2.13, 2.09, 1.95, 2.01, 1.91, 1.91, 1.97, 2, 1.89, 1.96, 1.98, 2.01, 2.18, 1.98, 2, 2.16, 2.15, 2.25, 2.42, 2.3, 2.39, 2.52, 2.51, 2.5, 2.52, 2.45, 2.31, 2.38, 2.45, 2.43, 2.46, 2.45, 2.56, 2.73, 2.82, 2.8, 2.79, 2.7, 2.66, 2.77, 2.72, 2.72, 2.69, 2.63, 2.57, 2.57, 2.38, 2.22, 2.22, 2.14, 2.23, 2.19, 2.14, 2.12, 2.11, 1.98, 1.86, 1.87, 1.86, 1.76, 1.62, 1.61, 1.63, 1.64, 1.56, 1.63, 1.67, 1.71, 1.73, 1.66]
exxon_stock_pr.reverse()
# Shell stock market price https://www.macrotrends.net/stocks/charts/RDS.B/royal-dutch-shell/stock-price-history
# Annual average stock price 
# 1988-2020
shell_stock_pr = [43.5805, 61.6673, 68.1272, 58.6596, 51.2054, 57.9991, 78.8613, 69.0977, 71.109, 70.1714, 56.8353, 51.9192, 66.7149, 75.8555, 69.2618, 59.6673, 44.3243, 38.485, 40.9025, 47.6157, 48.5519, 43.8304, 39.9019, 75.1956, 87.6566, 71.5944, 65.4763, 56.9945, 52.6794, 53.1449, 49.6713, 41.0117, 71.5844]
shell_stock_pr.reverse()
# Schlumberger  stock market price https://www.macrotrends.net/stocks/charts/SLB/schlumberger/stock-price-history
# Annual average stock price 
# 1982-2020
schlb_stock_pr = [25.4426, 38.893, 63.0249, 71.0414, 77.1398, 81.8332, 98.7178, 80.8276, 71.1588, 80.5805, 65.1799, 53.4554, 82.2184, 83.7735, 62.4011, 39.4465, 31.2243, 22.6196, 23.9534, 28.8248, 37.3738, 29.6174, 31.9293, 34.0197, 21.2591, 15.5755, 14.147, 15.4975, 15.691, 15.7538, 13.9662, 10.1767, 8.5389, 10.1573, 8.0186, 9.3184, 11.4812, 12.4312, 10.5703]
schlb_stock_pr.reverse()
# Halliburton stock market price https://www.macrotrends.net/stocks/charts/HAL/halliburton/stock-price-history
# Annual average stock price 
# 1973-2020
hallb_stock_pr = [15.0171, 24.4093, 43.5441, 46.3878, 41.897, 41.1779, 58.7275, 45.1132, 33.2161, 43.0962, 31.4233, 22.9544, 36.1681, 34.6078, 34.3181, 25.7396, 15.9055, 11.2625, 7.8105, 16.576, 21.5809, 19.8336, 20.1905, 21.6191, 13.7241, 9.9066, 8.0271, 8.9533, 7.2551, 9.9101, 11.8774, 8.5125, 7.3139, 8.4325, 5.6327, 7.1513, 8.7139, 9.5036, 8.1537, 15.8178, 14.7145, 8.9262, 7.931, 7.5604, 7.3108, 6.3368, 5.9218, 6.5036]
hallb_stock_pr.reverse()
# Baker Hughes stock market price digitized from https://www.fool.com/quote/nyse/baker-hughes-company/bkr/#InteractiveChart
# Annual average stock price 
# 1975-2020
bkr_stock_pr = [9.095744681, 11.96808511, 11.96808511, 11.77659574, 16.08510638, 28.14893617, 51.79787234, 40.88297872, 21.82978723, 18, 16.27659574, 15.22340426, 10.81914894, 13.59574468, 14.07446809, 25.56382979, 26.32978723, 21.44680851, 20.0106383, 22.0212766, 18.67021277, 22.59574468, 38.0106383, 41.93617021, 18.67021277, 24.12765957, 38.77659574, 36, 29.87234043, 33.03191489, 43.37234043, 61.75531915, 69.41489362, 78.41489362, 30.92553191, 42.89361702, 55.72340426, 49.69148936, 42.22340426, 57.15957447, 59.07446809, 49.40425532, 65.68085106, 30.73404255, 23.26595745, 21.92553191]



s_bkr_s_pr = list(range(1975, 2021, 1))
s_hallb_s_pr = list(range(1973, 2021, 1))
s_schlb_s_pr = list(range(1982, 2021, 1))
s_shell_s_pr = list(range(1988, 2021, 1))
s_exx_s_pr = list(range(0, 701, 1))
s_exx_s_pr = [i*1/12 + 1962 for i in s_exx_s_pr]

norm_basis = aver_pages_SEG

s_seg = list(range(1982, 2020, 1))
s_eage= list(range(2006, 2020, 1))
s_spe = list(range(1990, 2020, 1))
s_fr  = list(range(1960, 2020, 1))
s_spe[7] = None


#  Makes list of zeros of the corresponding length
def zerolistmaker_1(n):
    listofzeros = [0] * n
    return listofzeros

#  This procedure sorts a dictionary
def sorted_dictionary(d):
    sorted_d = sorted(d.items(), key=lambda x: x[1])
    return sorted_d 

# The procedure to make list of zeros
def zerolistmaker(norm_basis):
    listofzeros = [0] * len(norm_basis)
    return listofzeros
# The procedure to convert strings to floats
def make_float(my_list):
    outputlist = []
    for item in my_list:
        if outputlist is []:
            outputlist[0] = float(item)
        else:
            outputlist.append(float(item))
    return outputlist
# Summ of all the elements in one list to find groups of words impact
def sum_of_lists(input):
    output = zerolistmaker(norm_basis)
    for item in input:
        output = [x + y  for x, y in zip(output, item)]
    return output

# def industry_with_oil_price():
   
def build_org_figs_all_societies():
   
    fontsize_det = 13
    start_year = 1982
    end_year = 2019
# Academy dictionaty
    conn = sqlite3.connect('Academy_by_Country.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Academy")
    data_aca=cursor.fetchall()
    academy_dict = {}
    
    aff_dict_SEG = {}
    aff_dict_SPE = {}
    aff_dict_EAGE = {}
    
    aff_dict_SPE_check = {}
    
    for element in data_aca:
        academy_dict[element[0]] = eval(element[1])
# Industry dictionaty
    conn = sqlite3.connect('Industry.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Industry")
    data_ind=cursor.fetchall()
    industry_dict = {}
    for element in data_ind:
        industry_dict[element[0]] = eval(element[1])
    cursor.close()
    conn.close()

# Data for printing (SEG) 1982 - 2019
    conn = sqlite3.connect('SEG_affiliations_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SEG_affiliations_data")
    data_aff=cursor.fetchall()
    
    for element in data_aff:
        aff_dict_SEG[element[0]] = [i / j for i, j in zip(eval(element[1]), aver_coauth_numb_SEG)]
    
    cursor.close()
    conn.close()
    data_aff=[]

# Data for printing (SPE) 1990 - 2019
    conn = sqlite3.connect('SPE_affiliations_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SPE_affiliations_data")
    data_aff=cursor.fetchall()
    
    for element in data_aff:
        aff_dict_SPE[element[0]] = [i / j for i, j in zip(eval(element[1]), aver_coauth_numb_SPE)]
        aff_dict_SPE_check[element[0]] = eval(element[1])
    
    cursor.close()
    conn.close()
    data_aff=[]
    
# Data for printing (EAGE) 2006 - 2019
    conn = sqlite3.connect('EAGE_affiliations_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EAGE_affiliations_data")
    data_aff=cursor.fetchall()
    
    
    for element in data_aff:
        if element[0] == None: 
            pass
        else:
            aff_dict_EAGE[element[0]] = [i / j for i, j in zip(eval(element[1]), aver_coauth_numb_EAGE[5:])]

    cursor.close()
    conn.close()
    
    acad_sum_SEG  = []
    acad_sum_EAGE = []
    acad_sum_SPE  = []
    
    ind_sum_SEG   = []
    ind_sum_EAGE  = []
    ind_sum_SPE   = []
    
    for key, value in aff_dict_SEG.items():
        if key in countr_dict.keys() and sum(value) > 0:

            if acad_sum_SEG == []:
                acad_sum_SEG = value
            else:
                acad_sum_SEG = [i + j for i, j in zip(acad_sum_SEG, value)]
        else:
            
            if ind_sum_SEG == []:
                ind_sum_SEG = value
            else:
                ind_sum_SEG = [i + j for i, j in zip(ind_sum_SEG, value)]
    
    acad_sum_SEG_no_chn = [i - j for i, j in zip(acad_sum_SEG, aff_dict_SEG["China"])]
    
    
    for key, value in aff_dict_EAGE.items():
        if key in countr_dict.keys() and sum(value) > 0:
 
            if acad_sum_EAGE == []:
                acad_sum_EAGE = value
            else:
                acad_sum_EAGE = [i + j for i, j in zip(acad_sum_EAGE, value)]
        else:
            
            if ind_sum_EAGE == []:
                ind_sum_EAGE = value
            else:
                ind_sum_EAGE = [i + j for i, j in zip(ind_sum_EAGE, value)]
    
    
    acad_sum_EAGE_no_chn = [i - j for i, j in zip(acad_sum_EAGE, aff_dict_EAGE["China"])]


    for key, value in aff_dict_SPE.items():
        if key in countr_dict.keys() and sum(value) > 0:
            # print (key, '==', sum(value))
            if acad_sum_SPE == []:
                acad_sum_SPE = value
            else:
                acad_sum_SPE = [i + j for i, j in zip(acad_sum_SPE, value)]
        elif key != countr_dict.keys() and sum(value) > 0:
            if ind_sum_SPE == []:
                ind_sum_SPE = value
            else:
                ind_sum_SPE = [i + j for i, j in zip(ind_sum_SPE, value)]            
 
        else:
            
            if ind_sum_SPE == []:
                ind_sum_SPE = value
            else:
                ind_sum_SPE = [i + j for i, j in zip(ind_sum_SPE, value)]
               
    acad_sum_SPE_no_chn = [i - j for i, j in zip(acad_sum_SPE, aff_dict_SPE["China"])]
  
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    
    lns2 = plt.plot(s_spe, aff_dict_SPE["Baker Hughes"], 'c^-',linewidth=1.2 , markersize = 1.5, label="SPE")     
    lns1 = plt.plot(s_eage, aff_dict_EAGE["Baker Hughes"], 'r^-',linewidth=1.2 , markersize = 1.5, label="EAGE")    
    lns3 = plt.plot(s_seg, aff_dict_SEG["Baker Hughes"], 'b^-',linewidth=1.2 , markersize = 1.5, label="SEG")
   

    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Average number of publications')
    plt.legend(title='Baker Hughes', loc = 'upper left')
    plt.axis([1982, 2019, 0, 30], labelsize = fontsize_det)
   
    
    ax2 = fig.add_subplot(111, label="2", frame_on=False)
    # ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel('Stock market price, $', color=color)  # we already handled the x-label with ax1
    lns4 = ax2.plot(s_bkr_s_pr, bkr_stock_pr,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    # oil_price_infl
    # lns = lns1+lns2+lns3+lns4
    # labs = [l.get_label() for l in lns]
    # ax2.legend(lns, labs, loc=0)
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()
    ax2.xaxis.set_label_position('top') 
    ax2.yaxis.set_label_position('right') 
    ax2.set_xlabel('Year', color="green") 
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.axis([1982, 2019, 0, 80], labelsize = fontsize_det)
    plt.savefig('K:\\python\\SQL\\images\\BKR_stock.png', dpi=300)
    # plt.show()
    plt.close()

 
    
    # # Printing total impact of companies and countries:
    # academia_only_dict = {}
    # industry_only_dict = {}
    # for key, value in aff_dict_SPE.items():
    #     if key in countr_dict.keys():
    #         academia_only_dict[key] = sum(value)
    #     else:
    #         industry_only_dict[key] = sum(value)
    # academia_only_dict = sorted_dictionary(academia_only_dict)
    # industry_only_dict = sorted_dictionary(industry_only_dict)
    
    # for element in reversed(industry_only_dict):
    #     print(element)
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    lns2 = plt.plot(s_spe, aff_dict_SPE["Halliburton"], 'c^-',linewidth=1.2 , markersize = 1.5, label="SPE")     
    lns3 = plt.plot(s_seg, aff_dict_SEG["Halliburton"], 'b^-',linewidth=1.2 , markersize = 1.5, label="SEG")
    lns1 = plt.plot(s_eage, aff_dict_EAGE["Halliburton"], 'r^-',linewidth=1.2 , markersize = 1.5, label="EAGE")    
    
   

    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Average number of publications')
    plt.legend(title='Halliburton', loc = 'upper left')
    plt.axis([1982, 2019, 0, 30], labelsize = fontsize_det)
   
    
    ax2 = fig.add_subplot(111, label="2", frame_on=False)
    # ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel('Stock market price, $', color=color)  # we already handled the x-label with ax1
    lns4 = ax2.plot(s_hallb_s_pr, hallb_stock_pr,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    # oil_price_infl
    # lns = lns1+lns2+lns3+lns4
    # labs = [l.get_label() for l in lns]
    # ax2.legend(lns, labs, loc=0)
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()
    ax2.xaxis.set_label_position('top') 
    ax2.yaxis.set_label_position('right') 
    ax2.set_xlabel('Year', color="green") 
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.axis([1980, 2017, 0, 60], labelsize = fontsize_det)
    plt.savefig('K:\\python\\SQL\\images\\Hallb_stock.png', dpi=300)
    # plt.show()
    plt.close()
    
 
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    lns2 = plt.plot(s_spe, aff_dict_SPE["Schlumberger"], 'c^-',linewidth=1.2 , markersize = 1.5, label="SPE")
    lns3 = plt.plot(s_seg, aff_dict_SEG["Schlumberger"], 'b^-',linewidth=1.2 , markersize = 1.5, label="SEG")
      
    lns1 = plt.plot(s_eage, aff_dict_EAGE["Schlumberger"], 'r^-',linewidth=1.2 , markersize = 1.5, label="EAGE")    
 
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Average number of publications')
    plt.legend(title='Schlumberger', loc = 'upper left')
    plt.axis([1982, 2019, 0, 80], labelsize = fontsize_det)
   
    
    ax2 = fig.add_subplot(111, label="2", frame_on=False)
    # ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel('Stock market price, $', color=color)  # we already handled the x-label with ax1
    lns4 = ax2.plot(s_schlb_s_pr, schlb_stock_pr,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    # oil_price_infl
    # lns = lns1+lns2+lns3+lns4
    # labs = [l.get_label() for l in lns]
    # ax2.legend(lns, labs, loc=0)
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()
    ax2.xaxis.set_label_position('top') 
    ax2.yaxis.set_label_position('right') 
    ax2.set_xlabel('Year', color="green") 
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.axis([1982, 2019, 0, 100], labelsize = fontsize_det)
    plt.savefig('K:\\python\\SQL\\images\\Schlb_stock.png', dpi=300)
    # plt.show()
    plt.close()
    
    
    
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
        
    lns1 = plt.plot(s_eage, aff_dict_EAGE["Shell International Exploration and Production Inc."], 'r^-',linewidth=1.2 , markersize = 1.5, label="EAGE")    
    lns3 = plt.plot(s_seg, aff_dict_SEG["Shell International Exploration and Production Inc."], 'b^-',linewidth=1.2 , markersize = 1.5, label="SEG")
    lns2 = plt.plot(s_spe, aff_dict_SPE["Shell International Exploration and Production Inc."], 'c^-',linewidth=1.2 , markersize = 1.5, label="SPE")

    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Average number of publications')
    plt.legend(title='Shell', loc = 'upper left')
    plt.axis([1982, 2019, 0, 40], labelsize = fontsize_det)
   
    
    ax2 = fig.add_subplot(111, label="2", frame_on=False)
    # ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel('Stock market price, $', color=color)  # we already handled the x-label with ax1
    lns4 = ax2.plot(s_shell_s_pr, shell_stock_pr,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    # oil_price_infl
    # lns = lns1+lns2+lns3+lns4
    # labs = [l.get_label() for l in lns]
    # ax2.legend(lns, labs, loc=0)
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()
    ax2.xaxis.set_label_position('top') 
    ax2.yaxis.set_label_position('right') 
    ax2.set_xlabel('Year', color="green") 
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.axis([1982, 2019, 0, 85], labelsize = fontsize_det)
    plt.savefig('K:\\python\\SQL\\images\\Shell_stock.png', dpi=300)
    # plt.show()
    plt.close()
    
    
    fig, ax1 = plt.subplots()
    color = 'tab:blue'

    lns3 = plt.plot(s_seg, aff_dict_SEG["ExxonMobil"], 'b^-',linewidth=1.2 , markersize = 1.5, label="SEG")
    lns2 = plt.plot(s_spe, aff_dict_SPE["ExxonMobil"], 'c^-',linewidth=1.2 , markersize = 1.5, label="SPE")
        
    lns1 = plt.plot(s_eage, aff_dict_EAGE["ExxonMobil"], 'r^-',linewidth=1.2 , markersize = 1.5, label="EAGE")    

    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Average number of publications')
    plt.legend(title='ExxonMobil', loc = 'upper left')
    plt.axis([1982, 2019, 0, 40], labelsize = fontsize_det)
   
    
    ax2 = fig.add_subplot(111, label="2", frame_on=False)
    # ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel('Stock market price, $', color=color)  # we already handled the x-label with ax1
    lns4 = ax2.plot(s_exx_s_pr, exxon_stock_pr,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    # oil_price_infl
    # lns = lns1+lns2+lns3+lns4
    # labs = [l.get_label() for l in lns]
    # ax2.legend(lns, labs, loc=0)
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()
    ax2.xaxis.set_label_position('top') 
    ax2.yaxis.set_label_position('right') 
    ax2.set_xlabel('Year', color="green") 
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.axis([1984, 2021, 0, 105], labelsize = fontsize_det)
    plt.savefig('K:\\python\\SQL\\images\\Exxon_stock.png', dpi=300)
    # plt.show()
    plt.close()
    
    quit()
    
    plt.rcdefaults()
    plt.figure(figsize=(8,5))
    
    lns3 = plt.plot(s_seg, aff_dict_SEG['China'], 'r^-',linewidth=1.2 , markersize = 1.5, label="SEG")
    lns2 = plt.plot(s_eage, aff_dict_EAGE['China'], 'c^-',linewidth=1.2 , markersize = 1.5, label="EAGE")
    lns1 = plt.plot(s_spe, aff_dict_SPE['China'], 'b^-',linewidth=1.2 , markersize = 1.5, label="SPE")    
    
    
    plt.grid(True)
    plt.xlabel('Year', fontsize = fontsize_det)
    plt.ylabel('Average number of publications', fontsize = fontsize_det)
    plt.legend(title = r'$\bf{China}$',  prop={'size': fontsize_det}, title_fontsize=fontsize_det, loc = 'upper left')
    # plt.yticks([30, 100, 200])
    # plt.yscale('log')

    
          
    plt.axis([1982, 2019, 0, 200])
    plt.grid(b=None, which='minor', axis='both')
    plt.tick_params(axis='both', which='major', labelsize=fontsize_det)
    plt.tick_params(axis='both', which='minor', labelsize=fontsize_det)

    
    plt.savefig('K:\\python\\SQL\\images\\China_SPE_SEG_EAGE.png', dpi=300)
    plt.show()

    quit() 
    


    plt.rcdefaults()
    plt.figure(figsize=(8,5))
    
    lns3 = plt.plot(s_seg, aff_dict_SEG['Canada'], 'r^-',linewidth=1.2 , markersize = 1.5, label="SEG")
    lns2 = plt.plot(s_eage, aff_dict_EAGE['Canada'], 'c^-',linewidth=1.2 , markersize = 1.5, label="EAGE")
    lns1 = plt.plot(s_spe, aff_dict_SPE['Canada'], 'b^-',linewidth=1.2 , markersize = 1.5, label="SPE")    
    
    
    plt.grid(True)
    plt.xlabel('Year', fontsize = fontsize_det)
    plt.ylabel('Average number of publications', fontsize = fontsize_det)
    plt.legend(title = r'$\bf{Canada}$',  prop={'size': fontsize_det}, title_fontsize=fontsize_det, loc = 'upper left')
    # plt.yticks([30, 100, 200])
    # plt.yscale('log')

    
          
    plt.axis([1982, 2019, 0, 43])
    plt.grid(b=None, which='minor', axis='both')
    plt.tick_params(axis='both', which='major', labelsize=fontsize_det)
    plt.tick_params(axis='both', which='minor', labelsize=fontsize_det)

    
    plt.savefig('K:\\python\\SQL\\images\\Canada_SPE_SEG_EAGE.png', dpi=300)
    plt.show()

    quit() 
    
    
    plt.rcdefaults()
    plt.figure(figsize=(8,5))
    lns2 = plt.plot(s_eage, aff_dict_EAGE['United Kingdom of Great Britain and Northern Ireland'], 'c^-',linewidth=1.2 , markersize = 1.5, label="EAGE")
    lns3 = plt.plot(s_seg, aff_dict_SEG['United Kingdom of Great Britain and Northern Ireland'], 'r^-',linewidth=1.2 , markersize = 1.5, label="SEG")
    lns1 = plt.plot(s_spe, aff_dict_SPE['United Kingdom of Great Britain and Northern Ireland'], 'b^-',linewidth=1.2 , markersize = 1.5, label="SPE")    
    
    
    plt.grid(True)
    plt.xlabel('Year', fontsize = fontsize_det)
    plt.ylabel('Average number of publications', fontsize = fontsize_det)
    plt.legend(title = r'$\bf{UK}$',  prop={'size': fontsize_det}, title_fontsize=fontsize_det, loc = 'upper left')
    # plt.yticks([30, 100, 200])
    plt.yscale('log')

    
          
    plt.axis([1982, 2019, 0, 83])
    plt.grid(b=None, which='minor', axis='both')
    plt.tick_params(axis='both', which='major', labelsize=fontsize_det)
    plt.tick_params(axis='both', which='minor', labelsize=fontsize_det)

    
    plt.savefig('K:\\python\\SQL\\images\\UK_SPE_SEG_EAGE.png', dpi=300)
    plt.show()

    quit() 
   
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
        
    plt.rcdefaults()
    plt.figure(figsize=(8,5))
    lns2 = plt.plot(s_eage, aff_dict_EAGE['France'], 'c^-',linewidth=1.2 , markersize = 1.5, label="EAGE")
    lns3 = plt.plot(s_seg, aff_dict_SEG['France'], 'r^-',linewidth=1.2 , markersize = 1.5, label="SEG")
    lns1 = plt.plot(s_spe, aff_dict_SPE['France'], 'b^-',linewidth=1.2 , markersize = 1.5, label="SPE")    

    
    plt.grid(True)
    plt.xlabel('Year', fontsize = fontsize_det)
    plt.ylabel('Average number of publications', fontsize = fontsize_det)
    plt.legend(title = r'$\bf{France}$',  prop={'size': fontsize_det}, title_fontsize=fontsize_det, loc = 'upper center')
    # plt.yticks([30, 100,0])
    # plt.yscale('log')
    plt.axis([1982, 2019, 0, 50])
    plt.tick_params(axis='both', which='major', labelsize=fontsize_det)
    plt.tick_params(axis='both', which='minor', labelsize=fontsize_det)    
    
    # ax2 = fig.add_subplot(111, label="2", frame_on=False)
    ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel('France crude oil productionl, BBL/D/1K', color=color, fontsize = fontsize_det)  # we already handled the x-label with ax1
    lns4 = ax2.plot(s_fr, france_cop,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="France oil production")
    # oil_price_infl
    # lns = lns1+lns2+lns3+lns4
    # labs = [l.get_label() for l in lns]
    # ax2.legend(lns, labs, loc=0)

    ax2.set_xlabel('Year', color="green") 
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.axis([1982, 2019, 0, 70], labelsize = fontsize_det)
    plt.tick_params(axis='both', which='major', labelsize=fontsize_det)
    plt.tick_params(axis='both', which='minor', labelsize=fontsize_det)

    plt.savefig('K:\\python\\SQL\\images\\france_SPE_SEG_EAGE_oprod.png', dpi=300)
    plt.show()
    plt.close()
    
    quit()    

    # quit()    
          
    # 
    # plt.grid(b=None, which='minor', axis='both')
    # plt.tick_params(axis='both', which='major', labelsize=fontsize_det)
    # plt.tick_params(axis='both', which='minor', labelsize=fontsize_det)

    
    # plt.savefig('K:\\python\\SQL\\images\\USA_SPE_SEG_EAGE.png', dpi=300)
    # plt.show()






    plt.rcdefaults()
    plt.figure(figsize=(8,5))
    lns3 = plt.plot(s_seg, aff_dict_SEG['United States of America'], 'r^-',linewidth=1.2 , markersize = 1.5, label="SEG")
    lns1 = plt.plot(s_spe, aff_dict_SPE['United States of America'], 'b^-',linewidth=1.2 , markersize = 1.5, label="SPE")    
    lns2 = plt.plot(s_eage, aff_dict_EAGE['United States of America'], 'c^-',linewidth=1.2 , markersize = 1.5, label="EAGE")
    
    plt.grid(True)
    plt.xlabel('Year', fontsize = fontsize_det)
    plt.ylabel('Average number of publications', fontsize = fontsize_det)
    plt.legend(title = r'$\bf{USA}$',  prop={'size': fontsize_det}, title_fontsize=fontsize_det, loc = 'lower left')
    plt.yticks([30, 100, 200])
    plt.yscale('log')

    
          
    plt.axis([1982, 2019, 10, 250])
    plt.grid(b=None, which='minor', axis='both')
    plt.tick_params(axis='both', which='major', labelsize=fontsize_det)
    plt.tick_params(axis='both', which='minor', labelsize=fontsize_det)

    
    plt.savefig('K:\\python\\SQL\\images\\USA_SPE_SEG_EAGE.png', dpi=300)
    plt.show()

    quit()    

    plt.rcdefaults()
    plt.figure(figsize=(8,5))
    lns1 = plt.plot(s_spe, aff_dict_SPE['Shell International Exploration and Production Inc.'], 'b^-',linewidth=1.2 , markersize = 1.5, label="Shell")    
    lns3 = plt.plot(s_spe, aff_dict_SPE['Chevron Energy Technology Company'], 'r^-',linewidth=1.2 , markersize = 1.5, label="Chevron")
    lns2 = plt.plot(s_spe, aff_dict_SPE['BP'], 'c^-',linewidth=1.2 , markersize = 1.5, label="BP")
    lns4 = plt.plot(s_spe, aff_dict_SPE['Saudi Aramco'], 'g^-',linewidth=1.2 , markersize = 1.5, label="Saudi Aramco")
    
    plt.grid(True)
    plt.xlabel('Year', fontsize = fontsize_det)
    plt.ylabel('Average number of publications', fontsize = fontsize_det)
    plt.legend(prop={'size': fontsize_det}, loc = 'upper left')
    plt.axis([1990, 2019, 0, 35])
    plt.tick_params(axis='both', which='major', labelsize=fontsize_det)
    plt.tick_params(axis='both', which='minor', labelsize=fontsize_det)
    
    plt.savefig('K:\\python\\SQL\\images\\shell_chev_bp_aramc.png', dpi=300)
    plt.show()
   

    
    plt.rcdefaults()
    plt.figure(figsize=(8,5))
    lns1 = plt.plot(s_spe, aff_dict_SPE['Schlumberger'], 'b^-',linewidth=1.2 , markersize = 1.5, label="Schlumberger")    
    lns3 = plt.plot(s_spe, aff_dict_SPE['Halliburton'], 'r^-',linewidth=1.2 , markersize = 1.5, label="Halliburton")
    lns2 = plt.plot(s_spe, aff_dict_SPE['Baker Hughes'], 'c^-',linewidth=1.2 , markersize = 1.5, label="Baker Hughes")

    plt.grid(True)
    plt.xlabel('Year', fontsize = fontsize_det)
    plt.ylabel('Average number of publications', fontsize = fontsize_det)
    plt.legend(prop={'size': fontsize_det})
    plt.axis([1990, 2019, 0, 50])
    plt.tick_params(axis='both', which='major', labelsize=fontsize_det)
    plt.tick_params(axis='both', which='minor', labelsize=fontsize_det)
    
    plt.savefig('K:\\python\\SQL\\images\\slb_hal_bh.png', dpi=300)
    plt.show()
    

    # plt.savefig('K:\\python\\SQL\\images\\All_Academia.png', dpi=300)
    # plt.show()
    

    # # plt.savefig('K:\\python\\SQL\\images\\All_Academia.png', dpi=300)

    # # plt.rcdefaults()
    
    # lns1 = plt.plot(s_eage, ind_sum_EAGE, 'r^-',linewidth=1.2 , markersize = 1.5, label="EAGE")    
    # lns3 = plt.plot(s_seg, ind_sum_SEG, 'b^-',linewidth=1.2 , markersize = 1.5, label="SEG")
    # lns2 = plt.plot(s_spe, ind_sum_SPE, 'g^-',linewidth=1.2 , markersize = 1.5, label="SPE")

    # plt.grid(True)
    # plt.xlabel('Year')
    # plt.ylabel('Average number of publications')
    # plt.legend(title='Industry')
    # plt.axis([1982, 2019, 100, 700], labelsize = fontsize_det)
    
    # # plt.savefig('K:\\python\\SQL\\images\\All_Industry.png', dpi=300)
    # # plt.show()
    
    

    # print([i + j for i, j in zip(ind_sum_EAGE, acad_sum_EAGE)])

    # plt.rcdefaults()
    
    # lns1 = plt.plot(s_seg, ind_sum_SEG, 'r^-',linewidth=1.2 , markersize = 1.5, label="Industry") 
    # lns3 = plt.plot(s_seg, acad_sum_SEG, 'b^-',linewidth=1.2 , markersize = 1.5, label="Academia")
    # lns2 = plt.plot(s_seg, acad_sum_SEG_no_chn, 'g^-',linewidth=1.2 , markersize = 1.5, label="Academia without China")
   
    
    # plt.grid(True)
    # plt.xlabel('Year')
    # plt.ylabel('Average number of publications')
    # plt.legend(title='SEG')
    # plt.axis([1982, 2019, 0, 650], labelsize = fontsize_det)
    # # plt.savefig('K:\\python\\SQL\\images\\SEG_AcInd.png', dpi=300)
    # # plt.show()

 

    # plt.rcdefaults()
    # lns1 = plt.plot(s_eage, ind_sum_EAGE, 'r^-',linewidth=1.2 , markersize = 1.5, label="Industry")
    # lns3 = plt.plot(s_eage, acad_sum_EAGE, 'b^-',linewidth=1.2 , markersize = 1.5, label="Academia")
    # lns2 = plt.plot(s_eage, acad_sum_EAGE_no_chn, 'g^-',linewidth=1.2 , markersize = 1.5, label="Academia without China")
    
    # plt.grid(True)
    # plt.xlabel('Year')
    # plt.ylabel('Average number of publications')
    # plt.legend(title='EAGE')
    # plt.axis([2006, 2019, 0, 750], labelsize = fontsize_det)
    
    # # plt.savefig('K:\\python\\SQL\\images\\EAGE_AcInd.png', dpi=300)
    # # plt.show()
  


    # plt.rcdefaults()
    
    # lns1 = plt.plot(s_spe, ind_sum_SPE, 'g^-',linewidth=1.2 , markersize = 1.5, label="Industry")
    # lns3 = plt.plot(s_spe, acad_sum_SPE, 'b^-',linewidth=1.2 , markersize = 1.5, label="Academia")
    # lns2 = plt.plot(s_spe, acad_sum_SPE_no_chn, 'r^-',linewidth=1.2 , markersize = 1.5, label="Academia without China")
    
    # plt.grid(True)
    # plt.xlabel('Year')
    # plt.ylabel('Average number of publications')
    # plt.legend(title='SPE')
    # plt.axis([1990, 2019, 0, 350], labelsize = fontsize_det)
    # # plt.savefig('K:\\python\\SQL\\images\\SPE_AcInd.png', dpi=300)
    # # plt.show()
 
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
        
    lns1 = plt.plot(s_eage, ind_sum_EAGE, 'r^-',linewidth=1.2 , markersize = 1.5, label="EAGE")    
    lns3 = plt.plot(s_seg, ind_sum_SEG, 'b^-',linewidth=1.2 , markersize = 1.5, label="SEG")
    lns2 = plt.plot(s_spe, ind_sum_SPE, 'c^-',linewidth=1.2 , markersize = 1.5, label="SPE")

    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Average number of publications')
    plt.legend(title='Industry', loc = 'upper center')
    plt.axis([1982, 2019, 100, 700], labelsize = fontsize_det)
        
    s_OP = list(range(1979, 2021, 1))
    
    
    
    ax2 = fig.add_subplot(111, label="2", frame_on=False)
    # ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel('Inflation adjusted price of oil, $', color=color)  # we already handled the x-label with ax1
    lns4 = ax2.plot(s_OP, oil_price_infl,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    # oil_price_infl
    # lns = lns1+lns2+lns3+lns4
    # labs = [l.get_label() for l in lns]
    # ax2.legend(lns, labs, loc=0)
    ax2.xaxis.tick_top()
    ax2.yaxis.tick_right()
    ax2.xaxis.set_label_position('top') 
    ax2.yaxis.set_label_position('right') 
    ax2.set_xlabel('Year', color="green") 
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.axis([1979, 2016, 0, 120], labelsize = fontsize_det)
    plt.savefig('K:\\python\\SQL\\images\\indus_op_plot.png', dpi=300)
    plt.show()
    plt.close()
    
    
    # for key, value in aff_dict_SPE.items():
    #     if key in countr_dict.keys():
    #         print('0000 ==', key, '==' , sum(value))
    #     else:
    #         print('1111 ==', key, '==' , sum(value))
            
            
    # for key, value in aff_dict_SPE.items():
    #     print(key, '==' ,sum(value))
    
    # plt.rcdefaults()
    # lns3 = plt.plot(s_spe, aff_dict_SPE["United States of America"], 'b^-',linewidth=1.2 , markersize = 1.5, label="USA")
    # lns2 = plt.plot(s_spe, aff_dict_SPE["France"], 'g^-',linewidth=1.2 , markersize = 1.5, label="Norway")
    # lns1 = plt.plot(s_spe, aff_dict_SPE["United Kingdom of Great Britain and Northern Ireland"], 'r^-',linewidth=1.2 , markersize = 1.5, label="Canada")
    # lns0 = plt.plot(s_spe, aff_dict_SPE["China"], 'y^-',linewidth=1.2 , markersize = 1.5, label="China")
    
    # plt.grid(True)
    # plt.xlabel('Year')
    # plt.ylabel('Average number of publications')
    # plt.legend(loc=0)
    # plt.axis([1990, 2019, 0, 100], labelsize = fontsize_det)

    # plt.show()
    # plt.close() 
    
    # pap_spe_num = [i + j for i, j in zip(acad_sum_SPE, ind_sum_SPE)]
    
    # check_sum = []
    # for key, value in aff_dict_SPE_check.items():
    #     if value[7] > 0:
    #         print(key, 'bingo')
        
    #     if check_sum == []:
    #         check_sum = value
    #     else:
    #         check_sum = [i + j for i, j in zip(check_sum, value)]   
    
    # for item in check_sum:
    #     print(item)
        
    # for item in pap_spe_num:
    #     print(item)
        # if key in aff_dict_EAGE.items():
        
        # if key in aff_dict_SPE.items():
        
    # print(countr_dict.keys())
        
    quit()    


    # list_ind = []
    # list_aca = []
    # for key, value in aff_dict.items():
    #     if key in industry_dict.keys():
    #         list_ind.append(value)
    #     if key in academy_dict.keys():
    #         list_aca.append(value)

    # print_ind = sum_of_lists(list_ind)
    # print_aca = sum_of_lists(list_aca)
    # print_aca_no_ch = [i - j for i, j in zip(print_aca, aff_dict["China"])]
    # s = list(range(start_year, end_year+1, 1))
    # fig, ax1 = plt.subplots()
    # color = 'tab:blue'
    # lns1 = plt.plot(s, print_aca, 'r*-',linewidth=1.2 , markersize = 1.5, label="Academia")
    # lns2 = plt.plot(s, print_ind,'c>-',  linewidth=1.2 , markersize = 1.5, label="Industry")
    # lns3 = plt.plot(s, print_aca_no_ch, 'b^-',linewidth=1.2 , markersize = 1.5, label="Academia without China")
    # plt.grid(True)
    # plt.xlabel('Year')
    # plt.ylabel('Average number of publications')
    # # plt.legend()
    # plt.axis([1982, 2019, 0, 650], labelsize = fontsize_det)
    # ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    # color = 'tab:green'
    # ax2.set_ylabel('Price, $', color=color)  # we already handled the x-label with ax1
    # lns4 = ax2.plot(s, oil_price,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    # lns = lns1+lns2+lns3+lns4
    # labs = [l.get_label() for l in lns]
    # ax2.legend(lns, labs, loc=0)
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # ax2.axis([1982, 2019, 0, 120], labelsize = fontsize_det)
    # plt.savefig('C:\\temp\\Tex\\MDPI_SEG\\images\\acad_indus_plot.png', dpi=300)
    # plt.close()
    # slb_EAGE = [25, 61, 60, 72, 68, 71, 124, 209, 285, 253, 164, 135, 147, 156]
    # slb_EAGE_norm = [i / j for i, j in zip(slb_EAGE, aver_coauth_numb_EAGE)]
    # slb_SPE = [30, 45, 40, 41, 43, 72, 45, 0, 63, 81, 110, 132, 161, 132, 152, 147, 168, 140, 128, 103, 169, 177, 184, 168, 137, 76, 171, 165, 129, 138]
    # slb_SPE_norm = [i / j for i, j in zip(slb_SPE, aver_coauth_numb_SEG)]
    
    # print(slb_EAGE_norm)
    
    plt.rcdefaults()
   # lns4 = plt.plot(s, aff_dict["BGP"], 'p--',linewidth=.6 , markersize = 1.5, label="BGP")
    
    fig, ax = plt.subplots(figsize=(8,5))
    plt.rcdefaults()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    
    lns1 = plt.plot(list(range(1982, 2020, 1)), aff_dict["Schlumberger"], 'b*-',linewidth=0.6 , markersize = 1.5,  label="Schlumberger_SEG")
    lns2 = plt.plot(list(range(1990, 2020, 1)), slb_SPE_norm, 'r^-',linewidth=.6 , markersize = 1.5, label="Schlumberger_SPE")
    lns3 = plt.plot(list(range(2006, 2020, 1)), slb_EAGE_norm, 'mx--', linewidth=.9 , markersize = 1.5, label="Schlumberger_EAGE")
      
    
    # plt.scatter(s, t, color='black')
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    # plt.title('Increase of number of co-authors with time')
    plt.grid(True)
    plt.axis([1982, 2019, 0, 90], labelsize =fontsize_det)
    # plt.yscale('log')
    plt.legend(prop={'size': fontsize_det})
    plt.savefig('K:\\python\\SQL\\images\\Schlumb.png', dpi=300)
    plt.show()
    plt.close()
    
    slb_EAGE = [55, 79, 52, 103, 39, 56, 104, 55, 53, 48, 39, 55, 66, 42]
    slb_EAGE_norm = [i / j for i, j in zip(slb_EAGE, aver_coauth_numb_EAGE)]
    slb_SPE = [9, 26, 33, 24, 31, 30, 68, 0, 28, 25, 12, 19, 38, 42, 43, 51, 73, 37, 29, 49, 44, 45, 48, 40, 101, 57, 101, 50, 48, 37]
    slb_SPE_norm = [i / j for i, j in zip(slb_SPE, aver_coauth_numb_SEG)]
    
    # print(slb_EAGE_norm)
    
    plt.rcdefaults()
   # lns4 = plt.plot(s, aff_dict["BGP"], 'p--',linewidth=.6 , markersize = 1.5, label="BGP")
    
    fig, ax = plt.subplots(figsize=(8,5))
    plt.rcdefaults()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    
    lns1 = plt.plot(list(range(1982, 2020, 1)), aff_dict["Shell International Exploration and Production Inc."], 'b*-',linewidth=0.6 , markersize = 1.5,  label="Shell_SEG")
    lns2 = plt.plot(list(range(1990, 2020, 1)), slb_SPE_norm, 'r^-',linewidth=.6 , markersize = 1.5, label="Shell_SPE")
    lns3 = plt.plot(list(range(2006, 2020, 1)), slb_EAGE_norm, 'mx--', linewidth=.9 , markersize = 1.5, label="Shell_EAGE")
      
    
    # plt.scatter(s, t, color='black')
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    # plt.title('Increase of number of co-authors with time')
    plt.grid(True)
    plt.axis([1982, 2019, 0, 40], labelsize =fontsize_det)
    # plt.yscale('log')
    plt.legend(prop={'size': fontsize_det})
    plt.savefig('K:\\python\\SQL\\images\\Shell.png', dpi=300)
    plt.show()
    plt.close()


    slb_EAGE = [1, 8, 9, 12, 13, 18, 30, 20, 30, 35, 7, 59, 47, 66]
    slb_EAGE_norm = [i / j for i, j in zip(slb_EAGE, aver_coauth_numb_EAGE)]
    slb_SPE = [0, 0, 0, 0, 2, 0, 1, 0, 22, 23, 16, 51, 41, 42, 36, 28, 62, 47, 41, 23, 27, 20, 46, 36, 17, 26, 139, 34, 29, 10]
    slb_SPE_norm = [i / j for i, j in zip(slb_SPE, aver_coauth_numb_SEG)]
    
     # print(slb_EAGE_norm)
    
    plt.rcdefaults()
    # lns4 = plt.plot(s, aff_dict["BGP"], 'p--',linewidth=.6 , markersize = 1.5, label="BGP")
    
    fig, ax = plt.subplots(figsize=(8,5))
    plt.rcdefaults()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)

    lns1 = plt.plot(list(range(1982, 2020, 1)), aff_dict["Saudi Aramco"], 'b*-',linewidth=0.6 , markersize = 1.5,  label="Saudi Aramco_SEG")
    lns2 = plt.plot(list(range(1990, 2020, 1)), slb_SPE_norm, 'r^-',linewidth=.6 , markersize = 1.5, label="Saudi Aramco_SPE")
    lns3 = plt.plot(list(range(2006, 2020, 1)), slb_EAGE_norm, 'mx--', linewidth=.9 , markersize = 1.5, label="Saudi Aramco_EAGE")
      
    
     # plt.scatter(s, t, color='black')
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    # plt.title('Increase of number of co-authors with time')
    plt.grid(True)
    plt.axis([1982, 2019, 0, 45], labelsize =fontsize_det)
     # plt.yscale('log')
    plt.legend(prop={'size': fontsize_det})
    plt.savefig('K:\\python\\SQL\\images\\Shaudi Aramco.png', dpi=300)
    plt.show()
    plt.close()   
    
    
    quit()
    # plt.plot(list(range(1990, 1997, 1)), aver_coauth_numb_SPE[:7], 'c-', label="SPE")
    # plt.plot(, aver_coauth_numb_SPE[8:], 'c-')
    # plt.plot(s, aver_coauth_numb_SEG, 'b-', label="SEG")

    # plt.plot(, aver_coauth_numb_EAGE, 'r-', label="EAGE")   
    
    
    # plt.grid(True)


    # x = [2022, 2022, 2018]
    # y = [1, 4, 3.5]
    
    # label_x = 2022
    # label_y = 45
    # arrow_x = 2000
    # arrow_y = 46

    # arrow_properties = dict(
    # color="blue", width=0.25,
    # headwidth=8, shrink=0.04)
    # # headwidth=4, shrink=0.1)
 
    # quit()
    # ax = plt.gca()
    # ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    # ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)


    # plt.xlabel('Year', fontsize=fontsize_det)
    # plt.ylabel('Average number of publications', fontsize=fontsize_det)
    # plt.axis([1982, 2019, 0, 65], labelsize = fontsize_det)
    # ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    # ax2.axis([1982, 2019, 0, 120])
    # ax2.tick_params(axis='y', labelsize=fontsize_det)
    # color = 'tab:green'
    # ax2.set_ylabel('Price, $', color=color, size = 13)  # we already handled the x-label with ax1
    # lns5 = ax2.plot(s, oil_price,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    # lns = lns1+lns2+lns3+lns4+lns5
    # labs = [l.get_label() for l in lns]
    # ax2.legend(lns, labs, loc=0, fontsize=fontsize_det)
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.tight_layout() 

    # plt.savefig('K:\\python\\SQL\\images\\oil_service.png', dpi=300)
    # plt.show()
    # plt.close()
    
    # plt.rcdefaults()
    # fig, ax = plt.subplots(figsize=(10,5))
    # plt.plot(s, aff_dict["Petrochina"], 'c*-',linewidth=0.7 , markersize = 1.5,  label="PetroChina")
    # plt.plot(s, aff_dict["Shell International Exploration and Production Inc."], 'g-o',linewidth=0.5 , markersize = 1.5, label="Shell")
    # plt.plot(s, aff_dict["Saudi Aramco"], 'b--', linewidth=0.9 , markersize = 1.5, label="Saudi Aramco")
    # plt.plot(s, aff_dict["ExxonMobil"], 'r*-',linewidth=0.7 , markersize = 1.5,  label="ExxonMobil")
    # plt.plot(s, aff_dict["Total"], 'y^-',linewidth=1.2 , markersize = 1.5, label="Total")
   
    # ax = plt.gca()

    # x = [2022, 2022, 2018]
    # y = [1, 4, 3.5]
    
    
    # label_x = 2022
    # label_y = 2
    # arrow_x = 2014
    # arrow_y = 1

    # arrow_properties = dict(
    # # color="grey", width=0.5,
    # # headwidth=4, shrink=0.04)
    # color="blue", width=0.25,
    # headwidth=8, shrink=0.04)
    # # headwidth=4, shrink=0.1)
    # plt.annotate("Market valuation of ExxonMobil\ndecreased by 12%", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)

    
    # x = [2022, 2022, 2018]
    # y = [1, 4, 3.5]
    
    
    # label_x = 2022
    # label_y = 22
    # arrow_x = 2004.5
    # arrow_y = 27.5

    # arrow_properties = dict(
    # color="blue", width=0.25,
    # headwidth=8, shrink=0.04)
    # # headwidth=4, shrink=0.1)
    # plt.annotate("ExxonMobil reports\nnet income of 36 billion", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)

    # x = [2022, 2022, 2018]
    # y = [1, 4, 3.5]
    
    
    # label_x = 2022
    # label_y = 31
    # arrow_x = 2018
    # arrow_y = 32.5

    # arrow_properties = dict(
    # color="blue", width=0.25,
    # headwidth=8, shrink=0.04)
    # # headwidth=4, shrink=0.1)
    # plt.annotate("Saudi Aramco reports\n34.4% revenue increase", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)



    # ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    # ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)
    # plt.grid(True)
    # plt.xlabel('Year', fontsize=fontsize_det)
    # plt.ylabel('Average number of publications', fontsize=fontsize_det)
    # plt.axis([1982, 2019, 0, 35], labelsize = fontsize_det)
    # plt.legend(loc = "upper left", fontsize=fontsize_det)
    # plt.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.savefig('K:\\python\\SQL\\images\\oil_companies.png', dpi=300)
    # plt.show()
    # plt.close()

    # # img = Image.new('RGB', (3740, 1440))
    # # img1 = Image.open('K:\\python\\SQL\\images\\oil_service.png')
    # # img2 = Image.open('K:\\python\\SQL\\images\\oil_companies.png')
    # # img.paste(img1, (-40,0))
    # # img.paste(img2, (1830,0))
    # # img.save("K:\\python\\SQL\\images\\oil_and_service.png")
    # # img.show()
    # # img.close()

    # plt.rcdefaults()
    # fig, ax = plt.subplots(figsize=(10,5))
    # plt.plot(s, aff_dict["United States of America"], 'b*-',linewidth=0.7 , markersize = 1.5,  label="USA")
    # plt.plot(s, aff_dict["China"], 'g-o',linewidth=1 , markersize = 1.5, label="China")
    # plt.plot(s, aff_dict["Canada"], 'm--', linewidth=0.9 , markersize = 1.5, label="Canada")
    # plt.plot(s, aff_dict["Netherlands"], 'r*-',linewidth=0.7 , markersize = 1.5,  label="Netherlands")
    # # plt.plot(s, aff_dict["Total"], 'y^-',linewidth=1.2 , markersize = 1.5, label="Total")
    
    # ax = plt.gca()
    # ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    # ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)
    # plt.grid(True)
    
    
    # x = [2022, 2022, 2006]
    # y = [1, 4, 3.5]
    # label_x = 2022
    
    # label_y = 18
    # arrow_x = 2005.5
    # arrow_y = 23

    # arrow_properties = dict(
    # color="blue", width=0.25,
    # headwidth=8, shrink=0.04)

    # plt.annotate("Initiantion of the medium and\nLong-term Plan for R&D, China", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)

    # x = [2022, 2022, 2012]
    # y = [1, 4, 3.5]
    # label_x = 2022
    
    # label_y = 110
    # arrow_x = 2012.8
    # arrow_y = 115

    # arrow_properties = dict(
    # color="blue", width=0.25,
    # headwidth=8, shrink=0.04)
    
    # plt.annotate("15% increase in R&D spending", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)


    # x = [2022, 2022, 2018]
    # y = [1, 4, 3.5]
    # label_x = 2022
    
    # label_y = 215
    # arrow_x = 2018
    # arrow_y = 224

    # arrow_properties = dict(
    # color="blue", width=0.25,
    # headwidth=8, shrink=0.04)
    
    # plt.annotate("Reduction in state funding of\nhigher education, USA", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)




    # ax = plt.gca()

    
    # plt.xlabel('Year', fontsize=fontsize_det)
    # plt.ylabel('Average number of publications', fontsize=fontsize_det)
    # plt.axis([1982, 2019, 0, 230], labelsize = fontsize_det)
    # plt.legend(loc = "upper left", fontsize=fontsize_det)
    # plt.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.savefig('K:\\python\\SQL\\images\\4_first_countries.png', dpi=300)
    # plt.show()
    # plt.close()

    # plt.rcdefaults()
    # fig, ax = plt.subplots(figsize=(10,5))
    # plt.plot(s, aff_dict["France"], 'k*-',linewidth=1 , markersize = 1.5,  label="France")
    # plt.plot(s, aff_dict["United Kingdom of Great Britain and Northern Ireland"], 'c-.', linewidth=1.1 , markersize = 1.5, label="United Kingdom")
    # plt.plot(s, aff_dict["Germany"], 'y-o',linewidth=1.7 , markersize = 1.5, label="Germany")
    # plt.plot(s, aff_dict["Australia"], 'r--',linewidth=1.2 , markersize = 1.5,  label="Australia")
    # # plt.plot(s, aff_dict["Total"], 'y^-',linewidth=1.2 , markersize = 1.5, label="Total")

    # ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    # ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)
    # plt.grid(True)
    
    
    # x = [2022, 2022, 2018]
    # y = [1, 4, 3.5]
    
    # label_x = 2022
    # label_y = 22
    # arrow_x = 1988
    # arrow_y = 23

    # arrow_properties = dict(
    # color="blue", width=0.25,
    # headwidth=8, shrink=0.04)
    # # headwidth=4, shrink=0.1)
    # plt.annotate("Peaking of crude oil production,\nFrance: 1985-1995", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)



    # x = [2022, 2022, 2018]
    # y = [1, 4, 3.5]
    
    # label_x = 2022
    # label_y = 17
    # arrow_x = 1994.5
    # arrow_y = 18

    # arrow_properties = dict(
    # color="blue", width=0.25,
    # headwidth=8, shrink=0.04)
    # # headwidth=4, shrink=0.1)
    # plt.annotate("Peaking of crude oil production,\nUK: 1993-2004", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)



    # # x = [2022, 2022, 2018]
    # # y = [1, 4, 3.5]
    # # label_x = 2022
    
    # # label_y = 215
    # # arrow_x = 2017.5
    # # arrow_y = 224

    # # arrow_properties = dict(
    # # facecolor="black", width=0.5,
    # # headwidth=4, shrink=0.1)

    # # plt.annotate("Reduction of state funding of\nhigher education, USA*", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)

    
    
    # plt.xlabel('Year', fontsize=fontsize_det)
    # plt.ylabel('Average number of publications', fontsize=fontsize_det)
    # plt.axis([1982, 2019, 0, 37], labelsize = fontsize_det)
    # plt.legend(loc = "upper right", fontsize=fontsize_det)
    # plt.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.savefig('K:\\python\\SQL\\images\\4_second_countries.png', dpi=300)
    # plt.show()
    # plt.close()


    # # img = Image.new('RGB', (3740, 1440))
    # # img1 = Image.open('K:\\python\\SQL\\images\\4_first_countries.png')
    # # img2 = Image.open('K:\\python\\SQL\\images\\4_second_countries.png')
    # # img.paste(img1, (-40,0))
    # # img.paste(img2, (1850,0))
    # # img.save("K:\\python\\SQL\\images\\8_countries.png")
    # # img.show()
    # # img.close()
    
    # # for key, value in aff_dict.items():
    # #     if key in academy_dict.keys():
    # #         print(sum(value), key)




def co_aouth_figs():
    ax = plt.gca()
    fontsize_det = 13
   
    s = list(range(1982, 2020, 1))
    s1 = list(range(1980, 2017, 1))
    
    fig, ax = plt.subplots(figsize=(8,5))
    plt.rcdefaults()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    plt.plot(s1, ref_data, 'g-', label="Earth and planetary science")
    plt.plot(list(range(1990, 1997, 1)), aver_coauth_numb_SPE[:7], 'c-', label="SPE")
    plt.plot(list(range(1998, 2020, 1)), aver_coauth_numb_SPE[8:], 'c-')
    plt.plot(s, aver_coauth_numb_SEG, 'b-', label="SEG")

    plt.plot(list(range(2001, 2020, 1)), aver_coauth_numb_EAGE, 'r-', label="EAGE")        
     
    
    # plt.scatter(s, t, color='black')
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of authors per paper', fontsize=fontsize_det)
    # plt.title('Increase of number of co-authors with time')
    plt.grid(True)
    plt.axis([1982, 2019, 1.9, 4.8])
    # plt.yscale('log')
    plt.legend(prop={'size': fontsize_det})
    plt.savefig('K:\\python\\SQL\\images\\co_auth_all.png', dpi=300)
    plt.show()


def build_word_figs():
    fontsize_det = 13
    y_ax_label = 'No. of words/page'
    database_name = 'SEGgrams.sqlite'
    start_year = 1982
    left_border = 1990
    data_to_print = []
    legend_to_print = []
    summ_total = 0
    counter = 0
    data ={ "improve" : ['improve', 'strategy',  'efficiency', 'challenging', 'novel'],
            "proc_meth_decl" : ['Kirchhoff', 'CMP', 'NMO', 'velocity analysis', 'interferometry'],
           "proc_meth_grow"  : ['machine learning', 'broadband', 'seismicity',  'Marchenko', 'Markov', 'augmentation'],
            "most_popl_rocks" : ['shale', 'sandstone', 'carbonate',  'basalt', 'gneiss'],
           # "most_popl_rocks" : ['shale', 'sandstone', 'limestone',  'basalt', 'gneiss'],
            "some_rocks" : ['shale', 'carbonate', 'sandstone', 'limestone', 'volcanic' ],
            "shale_types" : ['Barnett', 'Eagle', 'Marcellus', 'Haynesville'],
            "hudr_frac" : ['hydraulic fracturing', 'frac', 'fracking', 'shale gas', 'gas shale', 'TOC', 'unconventional'],
            "conv_nn_deep" : ['convolutional neural', 'deep learning', 'artificial intelligence', 'neural network', 'field data' ],
            "nn_related" : ['convolutional neural', 'training data', 'machine learning', 'deep learning', 'training set', 'learning method', 'neural network' ],
            "most_grow_si" : ['learning', 'Marchenko', 'trained', 'generative', 'fibre', 'fiber'] ,
            "most_decl_si" : ['basalt', 'GPU', 'Barnett'],
            "most_grow_bi" : ['machine learning', 'training data', 'igneous rock', 'convolutional neural', 'computer vision', 'tight sandstone'],
            "most_decl_bi" : ['beam migration', 'source array', 'receiver depth', 'depth level', 'Barnett shale', 'receiver ghost'],
            "most_grow_tri" : ['convolutional neural network', 'seismic facies classification', 'distributed acoustic sensing', 'ground penetrating radar'],
            "most_decl_tri" : ['waveequation migration velocity', 'multiple attenuation algorithm', 'Eagle Ford Shale', 'Gassmann fluid substitution', 'towed streamer em'],
            "fwi_rtm_psdm2" : ['prestack depth migration', 'full waveform inversion', 'reverse time migration'],
            "fwi_rtm_psdm" : ['PSDM', 'FWI', 'RTM'],
            "stu_faculty" : ['student', 'faculty', 'researcher', 'engineer', 'scientist'],
            "sigrams_int2" : ['monitoring', 'efficiency', 'future', 'legacy'],
            "time_perm_jur_cret" : ['Cretaceous', 'Jurassic', 'Permian'], 
            "oil_gas_coal" : ['gas', 'water', 'oil',  'coal'],}

    for key, value in data.items():
        lists = value
        data_to_print = []
        legend_to_print = []
        for item in lists:
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            cursor.execute("SELECT words FROM WordsData WHERE words = ?", (item.lower(),))
            data_in=cursor.fetchall()
            if len(data_in)==0:
                print('\nThere is no entry named \'%s\''%item)
                data_to_print.append(zerolistmaker(norm_basis))
                legend_to_print.append(item)
            else:
                conn = sqlite3.connect(database_name)
                cursor = conn.cursor()
                cursor = conn.execute("SELECT * FROM WordsData WHERE words= ?", (item.lower(),))
                records = cursor.fetchone()
                conn.close()
                my_list = ast.literal_eval(records[1])
                data_to_print.append(make_float(my_list))
                legend_to_print = data[key]

        all_words_norm = []
        # We check if data is not zero
        for vals in data_to_print:
            if isinstance(vals, list):
        # We normalize each number of occurrences by number of pages at corresponding year
                words_norm = [i / j for i, j in zip(vals, norm_basis)]
                all_words_norm.append(words_norm)
                for part in vals:
                    summ_total = summ_total + part
            else:
                summ_total = summ_total + vals
        # We normalize each number of occurrences by number of pages at corresponding year
                words_norm = [i / j for i, j in zip(data_to_print, norm_basis)]
                all_words_norm = words_norm
        if summ_total < 0.00001:
            print('\nNone of the requsted words are present in the database.')
            print('Please, try again')
            quit()

        # Exclusions:
        if key == "hudr_frac":
            ts0 = all_words_norm[0]
            ts1 = all_words_norm[1]
            ts2 = all_words_norm[2]
            ts3 = all_words_norm[3]
            ts4 = all_words_norm[4]
            ts5 = all_words_norm[5]
            ts6 = all_words_norm[6]
            ts012 = []
            ts34 = []
            ts012 = [x + y + c for x, y, c in zip(ts0, ts1, ts2)]
            ts34 = [x + y  for x, y in zip(ts3, ts4)]
            ts = [ts012, ts34, ts5, ts6]
            all_words_norm = ts
            legend_to_print = ['fracking', 'shale gas', 'TOC', 'unconventional']
    # Here we are plotting the requestqed word(s)/phrase(s):
        colors = cm.rainbow(np.linspace(0.15, 1, len(all_words_norm)))
        ts = all_words_norm
        s = list(range(start_year, end_year+1, 1))
        # We set the appropriate scale for all the elements in the list
        for vals in ts:
        # The multiple entries case
            if isinstance(vals, list):
                maximum = [max(ts[ii]) for ii in range(0, len(ts))]
                minimum = [min(ts[ii]) for ii in range(0, len(ts))]
                maximum = max(maximum)
                minimum = min(minimum)
                maximum = maximum + 0.1*maximum
                minimum = minimum - 0.1*minimum
                for y, c in zip(ts, colors):
                    plt.plot(s, y, linewidth=1.1, color=c)
        # The single enrtry case
            else:
                maximum = max(ts)
                minimum = min(ts)
                maximum = maximum + 0.1*maximum
                minimum = minimum - 0.1*minimum
                plt.plot(s, ts, 'b-', linewidth=1)

        if minimum < 0:
            minimum = 0

        ax = plt.gca()
        ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
        ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)

        # Here we set the parameters of the figure
        plt.xlabel('Year', fontsize=fontsize_det)
        plt.ylabel(y_ax_label, fontsize=fontsize_det)
        plt.grid(True)
        plt.tight_layout()
        # The legend position
        if key == "fwi_rtm_psdm2":
            plt.legend(legend_to_print, loc = "upper right", fontsize=fontsize_det)
        elif key == "proc_meth_decl":
            plt.legend(legend_to_print, loc = "upper right", fontsize=fontsize_det)
        else:
            plt.legend(legend_to_print, loc = "upper left", fontsize=fontsize_det)
        # The range of the axes
        plt.axis([left_border, 2019, minimum, maximum], fontsize=fontsize_det)
        if len(lists[0]) > 3 and len(lists[1]) > 3:
            name = str(lists[0][:4] +'_' + lists[1][:4])
        else:
            name = str(lists[0][:3] +'_' + lists[1][:3])
        # print(name)
        plt.savefig('K:\\python\\SQL\\images\\'+key+'.png', dpi=300)
        # plt.show()
        plt.close()
        counter += 1

    # # img = Image.new('RGB', (3620, 1440))
    # img = Image.new('RGB', (3760, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\most_grow_si.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\most_decl_si.png')
    # img.paste(img1, (0,0))
    # # img.paste(img2, (1790,0))
    # img.paste(img2, (1910,0))
    # img.save("K:\\python\\SQL\\images\\si_grow_decl.png")
    # img.close()

    # # img = Image.new('RGB', (3620, 1440))
    # img = Image.new('RGB', (3760, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\most_grow_bi.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\most_decl_bi.png')
    # img.paste(img1, (0,0))
    # # img.paste(img2, (1790,0))
    # img.paste(img2, (1910,0))  
    # img.save("K:\\python\\SQL\\images\\bi_grow_decl.png")
    # img.close()
        
    # # img = Image.new('RGB', (3620, 1440))
    # img = Image.new('RGB', (3760, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\most_grow_tri.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\most_decl_tri.png')
    # img.paste(img1, (0,0))
    # # img.paste(img2, (1790,0))
    # img.paste(img2, (1910,0))
    # img.save("K:\\python\\SQL\\images\\tri_grow_decl.png")
    # img.close()

    # # img = Image.new('RGB', (3700, 1440))
    # img = Image.new('RGB', (3760, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\shale_types.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\hudr_frac.png')
    # img.paste(img1, (0,0))
    # # img.paste(img2, (1850,0))
    # img.paste(img2, (1910,0))
    # img.save("K:\\python\\SQL\\images\\shale_frac.png")
    # img.show()
    # img.close()

    img = Image.new('RGB', (3760, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\proc_meth_grow.png')
    img2 = Image.open('K:\\python\\SQL\\images\\proc_meth_decl.png')
    img.paste(img1, (0,0))
    # img.paste(img2, (1850,0))
    img.paste(img2, (1910,0))
    img.save("K:\\python\\SQL\\images\\proc_meth.png")
    img.show()
    img.close()



    # # img = Image.new('RGB', (3700, 1440))
    # img = Image.new('RGB', (3760, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\fwi_rtm_psdm2.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\fwi_rtm_psdm.png')
    # img.paste(img1, (0,0))
    # # img.paste(img2, (1850,0))
    # img.paste(img2, (1910,0))
    # img.save("K:\\python\\SQL\\images\\fwi_rtm_psdm_both.png")
    # img.show()
    # img.close()


    # img = Image.new('RGB', (3760, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\stu_faculty.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\sigrams_int2.png')
    # img.paste(img1, (0,0))
    # img.paste(img2, (1910,0))
    # img.save("K:\\python\\SQL\\images\\sigrams_int.png")
    # img.show()
    # img.close()

    # img = Image.new('RGB', (3760, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\conv_nn_deep.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\nn_related.png')
    # img.paste(img1, (0,0))
    # img.paste(img2, (1910,0))
    # img.save("K:\\python\\SQL\\images\\nn_related_all.png")
    # img.close()

    # img = Image.new('RGB', (3760, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\oil_gas_coal.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\time_perm_jur_cret.png')
    # img.paste(img1, (0,0))
    # img.paste(img2, (1910,0))
    # img.save("K:\\python\\SQL\\images\\fossil_time.png")
    # img.close()



   
def build_org_figs():
    fontsize_det = 13
    start_year = 1982
    end_year = 2019
# Academy dictionaty
    conn = sqlite3.connect('Academy_by_Country.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Academy")
    data_aca=cursor.fetchall()
    academy_dict = {}
    for element in data_aca:
        academy_dict[element[0]] = eval(element[1])
# Industry dictionaty
    conn = sqlite3.connect('Industry.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Industry")
    data_ind=cursor.fetchall()
    industry_dict = {}
    for element in data_ind:
        industry_dict[element[0]] = eval(element[1])
# Data for printing
    conn = sqlite3.connect('SEG_affiliations_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SEG_affiliations_data")
    data_aff=cursor.fetchall()
    aff_dict = {}
    for element in data_aff:
        aff_dict[element[0]] = [i / j for i, j in zip(eval(element[1]), aver_coauth_numb_SEG)]

    list_ind = []
    list_aca = []
    for key, value in aff_dict.items():
        if key in industry_dict.keys():
            list_ind.append(value)
        if key in academy_dict.keys():
            list_aca.append(value)

    print_ind = sum_of_lists(list_ind)
    print_aca = sum_of_lists(list_aca)
    print_aca_no_ch = [i - j for i, j in zip(print_aca, aff_dict["China"])]
    s = list(range(start_year, end_year+1, 1))
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    lns1 = plt.plot(s, print_aca, 'r*-',linewidth=1.2 , markersize = 1.5, label="Academia")
    lns2 = plt.plot(s, print_ind,'c>-',  linewidth=1.2 , markersize = 1.5, label="Industry")
    lns3 = plt.plot(s, print_aca_no_ch, 'b^-',linewidth=1.2 , markersize = 1.5, label="Academia without China")
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Average number of publications')
    # plt.legend()
    plt.axis([1982, 2019, 0, 650], labelsize = fontsize_det)
    ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:green'
    ax2.set_ylabel('Price, $', color=color)  # we already handled the x-label with ax1
    lns4 = ax2.plot(s, oil_price,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    lns = lns1+lns2+lns3+lns4
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=0)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.axis([1982, 2019, 0, 120], labelsize = fontsize_det)
    plt.savefig('C:\\temp\\Tex\\MDPI_SEG\\images\\acad_indus_plot.png', dpi=300)
    plt.close()

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(10,5))
    lns1 = plt.plot(s, aff_dict["Schlumberger"], 'b*-',linewidth=0.6 , markersize = 1.5,  label="Schlumberger")
    lns2 = plt.plot(s, aff_dict["WesternGeco"], 'r^-',linewidth=.6 , markersize = 1.5, label="WesternGeco")
    lns3 = plt.plot(s, aff_dict["CGG"], 'mx--', linewidth=.9 , markersize = 1.5, label="CGG")
    lns4 = plt.plot(s, aff_dict["BGP"], 'p--',linewidth=.6 , markersize = 1.5, label="BGP")
    
    plt.grid(True)


    x = [2022, 2022, 2018]
    y = [1, 4, 3.5]
    
    label_x = 2022
    label_y = 45
    arrow_x = 2000
    arrow_y = 46

    arrow_properties = dict(
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)
    # headwidth=4, shrink=0.1)
    plt.annotate("Schlumberger purchases WesternGeco", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)

    x = [2024, 2024, 2018]
    y = [1, 4, 3.5]
    y = [1, 1, 1]
    
    label_x = 2024
    label_y = 59
    arrow_x = 2014
    arrow_y = 62

    arrow_properties = dict(
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)
    # headwidth=4, shrink=0.1)
    plt.annotate("Schlumberger revenue for 2014\nreached a record $48.6 billion", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)

    x = [2024, 2024, 2018]
    y = [1, 4, 3.5]
    
    
    label_x = 2024
    label_y = 20
    arrow_x = 2014.5
    arrow_y = 36

    arrow_properties = dict(
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)
    # headwidth=4, shrink=0.1)
    plt.annotate("CGG reports cost reduction", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)


    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)


    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    plt.axis([1982, 2019, 0, 65], labelsize = fontsize_det)
    ax2 = plt.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.axis([1982, 2019, 0, 120])
    ax2.tick_params(axis='y', labelsize=fontsize_det)
    color = 'tab:green'
    ax2.set_ylabel('Price, $', color=color, size = 13)  # we already handled the x-label with ax1
    lns5 = ax2.plot(s, oil_price,'r--',  linewidth=1.5 , markersize = 1.5, color=color, label="OPEC crude oil price")
    lns = lns1+lns2+lns3+lns4+lns5
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=0, fontsize=fontsize_det)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.tight_layout() 

    plt.savefig('K:\\python\\SQL\\images\\oil_service.png', dpi=300)
    plt.show()
    plt.close()
    
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(10,5))
    plt.plot(s, aff_dict["Petrochina"], 'c*-',linewidth=0.7 , markersize = 1.5,  label="PetroChina")
    plt.plot(s, aff_dict["Shell International Exploration and Production Inc."], 'g-o',linewidth=0.5 , markersize = 1.5, label="Shell")
    plt.plot(s, aff_dict["Saudi Aramco"], 'b--', linewidth=0.9 , markersize = 1.5, label="Saudi Aramco")
    plt.plot(s, aff_dict["ExxonMobil"], 'r*-',linewidth=0.7 , markersize = 1.5,  label="ExxonMobil")
    plt.plot(s, aff_dict["Total"], 'y^-',linewidth=1.2 , markersize = 1.5, label="Total")
   
    ax = plt.gca()

    x = [2022, 2022, 2018]
    y = [1, 4, 3.5]
    
    
    label_x = 2022
    label_y = 2
    arrow_x = 2014
    arrow_y = 1

    arrow_properties = dict(
    # color="grey", width=0.5,
    # headwidth=4, shrink=0.04)
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)
    # headwidth=4, shrink=0.1)
    plt.annotate("Market valuation of ExxonMobil\ndecreased by 12%", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)

    
    x = [2022, 2022, 2018]
    y = [1, 4, 3.5]
    
    
    label_x = 2022
    label_y = 22
    arrow_x = 2004.5
    arrow_y = 27.5

    arrow_properties = dict(
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)
    # headwidth=4, shrink=0.1)
    plt.annotate("ExxonMobil reports\nnet income of 36 billion", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)

    x = [2022, 2022, 2018]
    y = [1, 4, 3.5]
    
    
    label_x = 2022
    label_y = 31
    arrow_x = 2018
    arrow_y = 32.5

    arrow_properties = dict(
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)
    # headwidth=4, shrink=0.1)
    plt.annotate("Saudi Aramco reports\n34.4% revenue increase", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)



    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)
    plt.grid(True)
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    plt.axis([1982, 2019, 0, 35], labelsize = fontsize_det)
    plt.legend(loc = "upper left", fontsize=fontsize_det)
    plt.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig('K:\\python\\SQL\\images\\oil_companies.png', dpi=300)
    plt.show()
    plt.close()

    # img = Image.new('RGB', (3740, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\oil_service.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\oil_companies.png')
    # img.paste(img1, (-40,0))
    # img.paste(img2, (1830,0))
    # img.save("K:\\python\\SQL\\images\\oil_and_service.png")
    # img.show()
    # img.close()

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(10,5))
    plt.plot(s, aff_dict["United States of America"], 'b*-',linewidth=0.7 , markersize = 1.5,  label="USA")
    plt.plot(s, aff_dict["China"], 'g-o',linewidth=1 , markersize = 1.5, label="China")
    plt.plot(s, aff_dict["Canada"], 'm--', linewidth=0.9 , markersize = 1.5, label="Canada")
    plt.plot(s, aff_dict["Netherlands"], 'r*-',linewidth=0.7 , markersize = 1.5,  label="Netherlands")
    # plt.plot(s, aff_dict["Total"], 'y^-',linewidth=1.2 , markersize = 1.5, label="Total")
    
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)
    plt.grid(True)
    
    
    x = [2022, 2022, 2006]
    y = [1, 4, 3.5]
    label_x = 2022
    
    label_y = 18
    arrow_x = 2005.5
    arrow_y = 23

    arrow_properties = dict(
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)

    plt.annotate("Initiantion of the medium and\nLong-term Plan for R&D, China", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)

    x = [2022, 2022, 2012]
    y = [1, 4, 3.5]
    label_x = 2022
    
    label_y = 110
    arrow_x = 2012.8
    arrow_y = 115

    arrow_properties = dict(
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)
    
    plt.annotate("15% increase in R&D spending", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)


    x = [2022, 2022, 2018]
    y = [1, 4, 3.5]
    label_x = 2022
    
    label_y = 215
    arrow_x = 2018
    arrow_y = 224

    arrow_properties = dict(
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)
    
    plt.annotate("Reduction in state funding of\nhigher education, USA", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)




    ax = plt.gca()

    
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    plt.axis([1982, 2019, 0, 230], labelsize = fontsize_det)
    plt.legend(loc = "upper left", fontsize=fontsize_det)
    plt.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig('K:\\python\\SQL\\images\\4_first_countries.png', dpi=300)
    plt.show()
    plt.close()

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(10,5))
    plt.plot(s, aff_dict["France"], 'k*-',linewidth=1 , markersize = 1.5,  label="France")
    plt.plot(s, aff_dict["United Kingdom of Great Britain and Northern Ireland"], 'c-.', linewidth=1.1 , markersize = 1.5, label="United Kingdom")
    plt.plot(s, aff_dict["Germany"], 'y-o',linewidth=1.7 , markersize = 1.5, label="Germany")
    plt.plot(s, aff_dict["Australia"], 'r--',linewidth=1.2 , markersize = 1.5,  label="Australia")
    # plt.plot(s, aff_dict["Total"], 'y^-',linewidth=1.2 , markersize = 1.5, label="Total")

    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)
    plt.grid(True)
    
    
    x = [2022, 2022, 2018]
    y = [1, 4, 3.5]
    
    label_x = 2022
    label_y = 22
    arrow_x = 1988
    arrow_y = 23

    arrow_properties = dict(
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)
    # headwidth=4, shrink=0.1)
    plt.annotate("Peaking of crude oil production,\nFrance: 1985-1995", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)



    x = [2022, 2022, 2018]
    y = [1, 4, 3.5]
    
    label_x = 2022
    label_y = 17
    arrow_x = 1994.5
    arrow_y = 18

    arrow_properties = dict(
    color="blue", width=0.25,
    headwidth=8, shrink=0.04)
    # headwidth=4, shrink=0.1)
    plt.annotate("Peaking of crude oil production,\nUK: 1993-2004", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)



    # x = [2022, 2022, 2018]
    # y = [1, 4, 3.5]
    # label_x = 2022
    
    # label_y = 215
    # arrow_x = 2017.5
    # arrow_y = 224

    # arrow_properties = dict(
    # facecolor="black", width=0.5,
    # headwidth=4, shrink=0.1)

    # plt.annotate("Reduction of state funding of\nhigher education, USA*", xy=(arrow_x, arrow_y),    xytext=(label_x, label_y),   arrowprops=arrow_properties, fontsize=fontsize_det)

    
    
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    plt.axis([1982, 2019, 0, 37], labelsize = fontsize_det)
    plt.legend(loc = "upper right", fontsize=fontsize_det)
    plt.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig('K:\\python\\SQL\\images\\4_second_countries.png', dpi=300)
    plt.show()
    plt.close()


    # img = Image.new('RGB', (3740, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\4_first_countries.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\4_second_countries.png')
    # img.paste(img1, (-40,0))
    # img.paste(img2, (1850,0))
    # img.save("K:\\python\\SQL\\images\\8_countries.png")
    # img.show()
    # img.close()
    
    # for key, value in aff_dict.items():
    #     if key in academy_dict.keys():
    #         print(sum(value), key)



def plot_hystogram():
    y_ax_label = 'No. of words/page'
    fontsize_det = 13
    conn = sqlite3.connect('SEGgrams.sqlite')
    cursor = conn.cursor()
    
    threewords = ['lateral velocity variation', 'seismic data processing', 'well log data', 'transversely isotropic medium', 'surface seismic data', 'seismic reflection data', 'shear wave velocity', 'migration velocity analysis', 'reverse time migration', 'full waveform inversion']
    twowords = ['wave propagation', 'velocity analysis', 'source receiver', 'field data', 'shear wave', 'depth migration', 'wave equation', 'data set', 'velocity model', 'seismic data']
    onewords = ['field',	'well', 'source',	'time',	'method',	'wave',	'model',	'velocity',	'seismic',	'data']

    w3_to_print = {}
    w3_leg_to_print = []
    w2_to_print = {}
    w2_leg_to_print = []
    w1_to_print = {}
    w1_leg_to_print = []
    # numb_pages
    for item in threewords:
        cursor.execute("SELECT * FROM WordsData WHERE words = ?", (item,))
        records = cursor.fetchone()
        my_list = [i / j for i, j in zip(eval(records[1]), aver_pages_SEG)]
        w3_to_print[records[0]] = sum(my_list[8:])/(len(aver_pages_SEG)-8)
    my_list = []
    for item in twowords:
        cursor.execute("SELECT * FROM WordsData WHERE words = ?", (item,))
        records = cursor.fetchone()
        my_list = [i / j for i, j in zip(eval(records[1]), aver_pages_SEG)]
        w2_to_print[records[0]] = sum(my_list[8:])/(len(aver_pages_SEG)-8)
    for item in onewords:
        cursor.execute("SELECT * FROM WordsData WHERE words = ?", (item,))
        records = cursor.fetchone()
        my_list = [i / j for i, j in zip(eval(records[1]), aver_pages_SEG)]
        w1_to_print[records[0]] = sum(my_list[8:])/(len(aver_pages_SEG)-8)

    # w3_to_print.reverse();    w2_to_print.reverse();    w1_to_print.reverse()
    # threewords.reverse();    twowords.reverse();    onewords.reverse()
    listofTuples3 = sorted(w3_to_print.items() ,  key=lambda x: x[1])
    listofTuples2 = sorted(w2_to_print.items() ,  key=lambda x: x[1])
    listofTuples1 = sorted(w1_to_print.items() ,  key=lambda x: x[1])
    w3_to_print = {}
    w2_to_print = {}
    w1_to_print = {}
    for item in listofTuples3: w3_to_print[item[0]] = float(item[1])
    for item in listofTuples2: w2_to_print[item[0]] = float(item[1])
    for item in listofTuples1: w1_to_print[item[0]] = float(item[1])

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(4.8,5))
    y_pos = np.arange(len(w3_to_print.keys()))
    ax.barh(y_pos, list(w3_to_print.values()), align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(w3_to_print.keys(), fontsize=fontsize_det)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(y_ax_label, fontsize=fontsize_det)
    plt.subplots_adjust(left=0.55, bottom=0.11, right=0.98, top=0.88, wspace=0.20, hspace=0.25)
    plt.tick_params(axis='x', labelsize=fontsize_det)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('K:\\python\\SQL\\images\\trigrams.png', dpi=300)
    plt.close()

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(3.5, 5))
    y_pos = np.arange(len(w2_to_print.keys()))
    ax.barh(y_pos, w2_to_print.values(), align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(w2_to_print.keys(), fontsize=fontsize_det)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(y_ax_label, fontsize=fontsize_det)
    plt.subplots_adjust(left=0.55, bottom=0.11, right=0.98, top=0.88, wspace=0.20, hspace=0.25)
    plt.tick_params(axis='x', labelsize=fontsize_det)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('K:\\python\\SQL\\images\\bigrams.png', dpi=300)
    plt.close()

    plt.show()
    fig, ax = plt.subplots(figsize= (2.7, 5))
    y_pos = np.arange(len(w1_to_print.keys()))
    ax.barh(y_pos, w1_to_print.values(), align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(w1_to_print.keys(), fontsize=fontsize_det)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(y_ax_label, fontsize=fontsize_det)
    plt.subplots_adjust(left=0.55, bottom=0.11, right=0.98, top=0.88, wspace=0.20, hspace=0.25)
    plt.tick_params(axis='x', labelsize=fontsize_det)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('K:\\python\\SQL\\images\\sigrams.png', dpi=300)
    plt.close()

    img = Image.new('RGB', (3150, 1460))
    img1 = Image.open('K:\\python\\SQL\\images\\trigrams.png')
    img2 = Image.open('K:\\python\\SQL\\images\\bigrams.png')
    img3 = Image.open('K:\\python\\SQL\\images\\sigrams.png')
    
    img.paste(img3, (0,0))
    img.paste(img2, (730,0))
    img.paste(img1, (1750,0))

    img.save("K:\\python\\SQL\\images\\grams_hyst.png")
    img.show()
    img.close()


def groups_printing():
    database_name = 'SEGgrams.sqlite'
    norm_basis = aver_pages_SEG
    start_year = 1982
    left_border = 1990
    fontsize_det = 13
    y_ax_label = 'No. of words/page'
    # We read the input data from the terminal
    # items = input('Please quote the word/phrase you want to check.\nExample1: \'machine learning\'\nIf more than one please use the list format:\nExample2:  [\'fwi\', \'well log\', \'convolutional neural network\', \'geophysics\']\nPlease type word(s)/phrase(s) you want to check here:\n')
    data_to_print = []
    legend_to_print = []
    total_printing_data = []
    summ_total = 0
    counter = 0
    data = [['sedimentary', 'clastic', 'breccia', 'conglomerate', 'sandstone', 'siltstone', 'shale', 'chert', 'flint', 'dolomite', 'limestone', 'carbonate', 'coal'],
    ['igneous', 'intrusive', 'diorite', 'gabbro', 'granite', 'pegmatite', 'peridotite', 'extrusive', 'andesite', 'basalt', 'dacite', 'obsidian', 'pumice', 'rhyolite', 'scoria', 'tuff', 'volcanics'],
    ['metamorphic', 'gneiss', 'phyllite', 'schist', 'slate', 'hornfels', 'marble', 'quartzite', 'novaculite', 'soapstone']
    ]
    # We consider the case when we have only one word/phrase to print
    # We consider the case when we have a number of word(s)/phrase(s) to print
    # plt.figure(figsize=(9,5))
    for lists in data:
        data_to_print = []
        legend_to_print = []
        for item in lists:
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            cursor.execute("SELECT words FROM WordsData WHERE words = ?", (item.lower(),))
            data_in=cursor.fetchall()
            if len(data_in)==0:
                print('\nThere is no entry named \'%s\''%item)
                data_to_print.append(zerolistmaker(norm_basis))
                legend_to_print.append(item)
            else:
                conn = sqlite3.connect(database_name)
                cursor = conn.cursor()
                cursor = conn.execute("SELECT * FROM WordsData WHERE words= ?", (item.lower(),))
                records = cursor.fetchone()
                end = time.time()
                conn.close()
                my_list = ast.literal_eval(records[1])
                data_to_print.append(make_float(my_list))
                legend_to_print = data[counter]
    
        all_words_norm = []
        # We check if data is not zero
        for vals in data_to_print:
            if isinstance(vals, list):
        # We normalize each number of occurrences by number of pages at corresponding year
                words_norm = [i / j for i, j in zip(vals, norm_basis)]
                all_words_norm.append(words_norm)
                for part in vals:
                    summ_total = summ_total + part
            else:
                summ_total = summ_total + vals
        # We normalize each number of occurrences by number of pages at corresponding year
                words_norm = [i / j for i, j in zip(data_to_print, norm_basis)]
                all_words_norm = words_norm
        if summ_total < 0.00001:
            print('\nNone of the requsted words are present in the database.')
            print('Please, try again')
    
        total_printing_data.append(all_words_norm)
    
    groups_to_print = []
    for element in total_printing_data:
        groups_to_print.append(sum_of_lists(element))
    
    # print(groups_to_print)
    legend_to_print = ['sedimentary', 'igneous', 'metamorphic']
    # Here we are plotting the requestqed word(s)/phrase(s):
    colors = cm.rainbow(np.linspace(0.15, 1, len(groups_to_print)))
    ts = groups_to_print
    s = list(range(start_year, end_year+1, 1))
    # We set the appropriate scale for all the elements in the list
    for vals in ts:
    # The multiple entries case
        if isinstance(vals, list):
            maximum = [max(ts[ii]) for ii in range(0, len(ts))]
            minimum = [min(ts[ii]) for ii in range(0, len(ts))]
            maximum = max(maximum)
            minimum = min(minimum)
            maximum = maximum + 0.1*maximum
            minimum = minimum - 0.1*minimum
            for y, c in zip(ts, colors):
                plt.plot(s, y, linewidth=1.1, color=c)
    # The single enrtry case
        else:
            maximum = max(ts)
            minimum = min(ts)
            maximum = maximum + 0.1*maximum
            minimum = minimum - 0.1*minimum
            plt.plot(s, ts, 'b-', linewidth=1)
    
    if minimum < 0:
        minimum = 0
    
    # Here we set the parameters of the figure
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)

    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel(y_ax_label, fontsize=fontsize_det)
    plt.grid(True)
    plt.tight_layout()
    # The legend position
    plt.legend(legend_to_print, loc = "lower left", fontsize=fontsize_det)
    # The range of the axes
    # plt.axis([left_border, 2019, minimum, maximum])
    plt.axis([left_border, 2019, 0.002, 1])
    # if len(lists[0]) > 3 and len(lists[1]) > 3:
    #     name = str(lists[0][:4] +'_' + lists[1][:4])
    # else:
    #     name = str(lists[0][:3] +'_' + lists[1][:3])
    # # print(name)
    plt.grid(b=True, which='minor', color='grey', linestyle='--', linewidth=0.35)
    plt.yscale('log')
    plt.savefig('K:\\python\\SQL\\images\\rock_types.png', dpi=300)
    # plt.show()
    plt.close()


    img = Image.new('RGB', (3700, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\rock_types.png')
    img2 = Image.open('K:\\python\\SQL\\images\\most_popl_rocks.png')
    img.paste(img1, (0,0))
    img.paste(img2, (1850,0))
    img.save("K:\\python\\SQL\\images\\rocks.png")
    img.show()
    img.close()

def groups_printing2():
    database_name = 'SEGgrams.sqlite'
    norm_basis = aver_pages_SEG
    start_year = 1982
    left_border = 1990
    fontsize_det = 13
    y_ax_label = 'No. of words/page'
    # We read the input data from the terminal
    # items = input('Please quote the word/phrase you want to check.\nExample1: \'machine learning\'\nIf more than one please use the list format:\nExample2:  [\'fwi\', \'well log\', \'convolutional neural network\', \'geophysics\']\nPlease type word(s)/phrase(s) you want to check here:\n')
    data_to_print = []
    legend_to_print = []
    total_printing_data = []
    summ_total = 0
    counter = 0
    data = [['seismic', 'seismics'],
        ['electromagnetic', 'em'],
    ['gravity', 'gravimetry', 'gravimetric', 'bouguer'],
    ['magnetic', 'geomagnetic'],
    ['logging', 'borehole geophysics']
    ]
    # We consider the case when we have only one word/phrase to print
    # We consider the case when we have a number of word(s)/phrase(s) to print
    # plt.figure(figsize=(9,5))
    for lists in data:
        data_to_print = []
        legend_to_print = []
        for item in lists:
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            cursor.execute("SELECT words FROM WordsData WHERE words = ?", (item.lower(),))
            data_in=cursor.fetchall()
            if len(data_in)==0:
                print('\nThere is no entry named \'%s\''%item)
                data_to_print.append(zerolistmaker(norm_basis))
                legend_to_print.append(item)
            else:
                conn = sqlite3.connect(database_name)
                cursor = conn.cursor()
                cursor = conn.execute("SELECT * FROM WordsData WHERE words= ?", (item.lower(),))
                records = cursor.fetchone()
                end = time.time()
                conn.close()
                my_list = ast.literal_eval(records[1])
                data_to_print.append(make_float(my_list))
                legend_to_print = data[counter]
    
        all_words_norm = []
        # We check if data is not zero
        for vals in data_to_print:
            if isinstance(vals, list):
        # We normalize each number of occurrences by number of pages at corresponding year
                words_norm = [i / j for i, j in zip(vals, norm_basis)]
                all_words_norm.append(words_norm)
                for part in vals:
                    summ_total = summ_total + part
            else:
                summ_total = summ_total + vals
        # We normalize each number of occurrences by number of pages at corresponding year
                words_norm = [i / j for i, j in zip(data_to_print, norm_basis)]
                all_words_norm = words_norm
        if summ_total < 0.00001:
            print('\nNone of the requsted words are present in the database.')
            print('Please, try again')
    
        total_printing_data.append(all_words_norm)
    
    groups_to_print = []
    for element in total_printing_data:
        groups_to_print.append(sum_of_lists(element))
    
    # print(groups_to_print)
    legend_to_print = [] 
    for element in data:
        legend_to_print.append(element[0])
    
    # ['seismic', 'electromagnetic', 'gravity', 'logging']
    # Here we are plotting the requestqed word(s)/phrase(s):
    colors = cm.rainbow(np.linspace(0.15, 1, len(groups_to_print)))
    ts = groups_to_print
    s = list(range(start_year, end_year+1, 1))
    # We set the appropriate scale for all the elements in the list
    for vals in ts:
    # The multiple entries case
        if isinstance(vals, list):
            maximum = [max(ts[ii]) for ii in range(0, len(ts))]
            minimum = [min(ts[ii]) for ii in range(0, len(ts))]
            maximum = max(maximum)
            minimum = min(minimum)
            maximum = maximum + 0.1*maximum
            minimum = minimum - 0.1*minimum
            for y, c in zip(ts, colors):
                plt.plot(s, y, linewidth=1.1, color=c)
    # The single enrtry case
        else:
            maximum = max(ts)
            minimum = min(ts)
            maximum = maximum + 0.1*maximum
            minimum = minimum - 0.1*minimum
            plt.plot(s, ts, 'b-', linewidth=1)
    
    if minimum < 0:
        minimum = 0
    
    # Here we set the parameters of the figure
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)

    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel(y_ax_label, fontsize=fontsize_det)
    plt.grid(True)
    plt.tight_layout()
    # The legend position
    # plt.legend(legend_to_print, loc = "lower left", fontsize=fontsize_det)
    plt.legend(legend_to_print, loc='best', bbox_to_anchor=(0.55, 0.48, 0.5, 0.5) , fontsize=fontsize_det)
    # The range of the axes
    # plt.axis([left_border, 2019, minimum, maximum])
    plt.axis([left_border, 2019, 0.03, 3])
    # if len(lists[0]) > 3 and len(lists[1]) > 3:
    #     name = str(lists[0][:4] +'_' + lists[1][:4])
    # else:
    #     name = str(lists[0][:3] +'_' + lists[1][:3])
    # # print(name)
    plt.grid(b=True, which='minor', color='grey', linestyle='--', linewidth=0.35)
    plt.yscale('log')
    plt.savefig('K:\\python\\SQL\\images\\geo_methods.png', dpi=300)
    plt.show()
    plt.close()


    img = Image.new('RGB', (3700, 1440))
    img1 = Image.open('K:\\python\\SQL\\images\\geo_methods.png')
    img2 = Image.open('K:\\python\\SQL\\images\\oil_gas_coal.png')
    img.paste(img1, (0,0))
    img.paste(img2, (1850,0))
    img.save("K:\\python\\SQL\\images\\methods_objects.png")
    img.show()
    img.close()

def groups_printing3():
    database_name = 'SEGgrams.sqlite'
    norm_basis = aver_pages_SEG
    start_year = 1982
    left_border = 1990
    fontsize_det = 13
    y_ax_label = 'No. of words/page'
    # We read the input data from the terminal
    # items = input('Please quote the word/phrase you want to check.\nExample1: \'machine learning\'\nIf more than one please use the list format:\nExample2:  [\'fwi\', \'well log\', \'convolutional neural network\', \'geophysics\']\nPlease type word(s)/phrase(s) you want to check here:\n')
    data_to_print = []
    legend_to_print = []
    total_printing_data = []
    summ_total = 0
    counter = 0
    data = [['FWI', 'full waveform inversion'],
        ['PSDM', 'prestack depth migration', ],
    ['RTM', 'reverse time migration'],
    ['CSEM', 'controlled source electromagnetic'],
    ]

    # We consider the case when we have only one word/phrase to print
    # We consider the case when we have a number of word(s)/phrase(s) to print
    # plt.figure(figsize=(9,5))
    for lists in data:
        data_to_print = []
        legend_to_print = []
        for item in lists:
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            cursor.execute("SELECT words FROM WordsData WHERE words = ?", (item.lower(),))
            data_in=cursor.fetchall()
            if len(data_in)==0:
                print('\nThere is no entry named \'%s\''%item)
                data_to_print.append(zerolistmaker(norm_basis))
                legend_to_print.append(item)
            else:
                conn = sqlite3.connect(database_name)
                cursor = conn.cursor()
                cursor = conn.execute("SELECT * FROM WordsData WHERE words= ?", (item.lower(),))
                records = cursor.fetchone()
                end = time.time()
                conn.close()
                my_list = ast.literal_eval(records[1])
                data_to_print.append(make_float(my_list))
                legend_to_print = data[counter]
    
        all_words_norm = []
        # We check if data is not zero
        for vals in data_to_print:
            if isinstance(vals, list):
        # We normalize each number of occurrences by number of pages at corresponding year
                words_norm = [i / j for i, j in zip(vals, norm_basis)]
                all_words_norm.append(words_norm)
                for part in vals:
                    summ_total = summ_total + part
            else:
                summ_total = summ_total + vals
        # We normalize each number of occurrences by number of pages at corresponding year
                words_norm = [i / j for i, j in zip(data_to_print, norm_basis)]
                all_words_norm = words_norm
        if summ_total < 0.00001:
            print('\nNone of the requsted words are present in the database.')
            print('Please, try again')
    
        total_printing_data.append(all_words_norm)
    
    groups_to_print = []
    for element in total_printing_data:
        groups_to_print.append(sum_of_lists(element))
    
    # print(groups_to_print)
    legend_to_print = [] 
    for element in data:
        legend_to_print.append(element[0])
    
    # ['seismic', 'electromagnetic', 'gravity', 'logging']
    # Here we are plotting the requestqed word(s)/phrase(s):
    colors = cm.rainbow(np.linspace(0.15, 1, len(groups_to_print)))
    ts = groups_to_print
    s = list(range(start_year, end_year+1, 1))
    # We set the appropriate scale for all the elements in the list
    for vals in ts:
    # The multiple entries case
        if isinstance(vals, list):
            maximum = [max(ts[ii]) for ii in range(0, len(ts))]
            minimum = [min(ts[ii]) for ii in range(0, len(ts))]
            maximum = max(maximum)
            minimum = min(minimum)
            maximum = maximum + 0.1*maximum
            minimum = minimum - 0.1*minimum
            for y, c in zip(ts, colors):
                plt.plot(s, y, linewidth=1.1, color=c)
    # The single enrtry case
        else:
            maximum = max(ts)
            minimum = min(ts)
            maximum = maximum + 0.1*maximum
            minimum = minimum - 0.1*minimum
            plt.plot(s, ts, 'b-', linewidth=1)
    
    if minimum < 0:
        minimum = 0
    
    # Here we set the parameters of the figure
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)

    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel(y_ax_label, fontsize=fontsize_det)
    plt.grid(True)
    plt.tight_layout()
    # The legend position
    plt.legend(legend_to_print, loc = "upper left", fontsize=fontsize_det)
    # plt.legend(legend_to_print, loc='best', bbox_to_anchor=(0.55, 0.48, 0.5, 0.5) , fontsize=fontsize_det)
    # The range of the axes
    # plt.axis([left_border, 2019, minimum, maximum])
    plt.axis([left_border, 2019, 0, 0.55])
    # if len(lists[0]) > 3 and len(lists[1]) > 3:
    #     name = str(lists[0][:4] +'_' + lists[1][:4])
    # else:
    #     name = str(lists[0][:3] +'_' + lists[1][:3])
    # # print(name)
    plt.grid(b=True, which='minor', color='grey', linestyle='--', linewidth=0.35)
    # plt.yscale('log')
    plt.savefig('K:\\python\\SQL\\images\\process_methods.png', dpi=300)
    plt.show()
    plt.close()


    # img = Image.new('RGB', (3700, 1440))
    # img1 = Image.open('K:\\python\\SQL\\images\\geo_methods.png')
    # img2 = Image.open('K:\\python\\SQL\\images\\oil_gas_coal.png')
    # img.paste(img1, (0,0))
    # img.paste(img2, (1850,0))
    # img.save("K:\\python\\SQL\\images\\particular_methods.png")
    # img.show()
    # img.close()
    
    
def france_prod():
    s = list(range(start_year, end_year+1, 1))
    conn = sqlite3.connect('SEG_affiliations_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SEG_affiliations_data")
    data_aff=cursor.fetchall()
    aff_dict = {}
    for element in data_aff:
        aff_dict[element[0]] = [i / j for i, j in zip(eval(element[1]), aver_coauth_numb_SEG)]

    plt.rcdefaults()

    plt.plot(s, aff_dict["France"], 'b*-',linewidth=0.7 , markersize = 1.5,  label="France")
    plt.plot(s, france_cop[22:], 'g-o',linewidth=1 , markersize = 1.5, label="France crude oil production")
    print(numpy.corrcoef(aff_dict["France"], france_cop[22:])[0, 1])
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = fontsize_det)
    ax.tick_params(axis = 'both', which = 'minor', labelsize = fontsize_det)
    plt.grid(True)
    plt.xlabel('Year', fontsize=fontsize_det)
    plt.ylabel('Average number of publications', fontsize=fontsize_det)
    plt.axis([1982, 2019, 0, 70], labelsize = fontsize_det)
    # plt.yscale('log')
    plt.legend(loc = "upper right", fontsize=fontsize_det)
    plt.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig('K:\\python\\SQL\\images\\France_COP.png', dpi=300)
    plt.show()
    plt.close()
 
def pieplot():
    
    database_name = 'SEGgrams.sqlite'
    norm_basis = aver_pages_SEG
    start_year = 1982
    left_border = 1990
    fontsize_det = 13

    # We read the input data from the terminal
    # items = input('Please quote the word/phrase you want to check.\nExample1: \'machine learning\'\nIf more than one please use the list format:\nExample2:  [\'fwi\', \'well log\', \'convolutional neural network\', \'geophysics\']\nPlease type word(s)/phrase(s) you want to check here:\n')
    data_to_print = []
    legend_to_print = []
    total_printing_data = []
    summ_total = 0
    counter = 0
    data = [['seismic', 'seismics'],
    ['magnetic', 'geomagnetic', 'aeromagnetic'],
    ['electromagnetic', 'em'],
    ['gravity', 'gravimetry', 'gravimetric'],
    ['electric', 'geoelectric'],
    ['logging', 'borehole geophysics'],
    ]
    # We consider the case when we have only one word/phrase to print
    # We consider the case when we have a number of word(s)/phrase(s) to print
    # plt.figure(figsize=(9,5))
    for lists in data:
        data_to_print = []
        legend_to_print = []
        for item in lists:
            conn = sqlite3.connect(database_name)
            cursor = conn.cursor()
            cursor.execute("SELECT words FROM WordsData WHERE words = ?", (item.lower(),))
            data_in=cursor.fetchall()
            if len(data_in)==0:
                print('\nThere is no entry named \'%s\''%item)
                data_to_print.append(zerolistmaker(norm_basis))
                legend_to_print.append(item)
            else:
                conn = sqlite3.connect(database_name)
                cursor = conn.cursor()
                cursor = conn.execute("SELECT * FROM WordsData WHERE words= ?", (item.lower(),))
                records = cursor.fetchone()
                end = time.time()
                conn.close()
                my_list = ast.literal_eval(records[1])
                data_to_print.append(make_float(my_list))
                legend_to_print = data[counter]
    
        all_words_norm = []
        # We check if data is not zero
        for vals in data_to_print:
            if isinstance(vals, list):
        # We normalize each number of occurrences by number of pages at corresponding year
                words_norm = [i / j for i, j in zip(vals, norm_basis)]
                all_words_norm.append(words_norm)
                for part in vals:
                    summ_total = summ_total + part
            else:
                summ_total = summ_total + vals
        # We normalize each number of occurrences by number of pages at corresponding year
                words_norm = [i / j for i, j in zip(data_to_print, norm_basis)]
                all_words_norm = words_norm
        if summ_total < 0.00001:
            print('\nNone of the requsted words are present in the database.')
            print('Please, try again')
    
        total_printing_data.append(all_words_norm)
    
    groups_to_print = []
    for element in total_printing_data:
        groups_to_print.append(sum_of_lists(element))
    
    legend_to_print = [] 
    sum_data = []
    
    for  listing in groups_to_print:
        sum_data.append(sum(listing[8:]))  
       
    for element in data:
        legend_to_print.append(element[0])
    
    fig, ax = plt.subplots(figsize=(9.2, 4.6), subplot_kw=dict(aspect="equal"))

   
    data = sum_data
    ingredients = legend_to_print
    # print(data) 
    # print(ingredients)
    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%".format(pct, absolute)
    
    # wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      # textprops=dict(color="black"))
    wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)
    ax.legend(wedges, ingredients,
              # title="Ingredients",
              loc="center left",
              fontsize=fontsize_det,
              bbox_to_anchor=(1, 0, 0.5, 1))

    # autotexts = [(-0.41456508615918247, 0.4337462268859864, '74.3%'), (0.11286151998255567, -0.5892896378753212, '7.5%'), (0.3637716954806089, -0.477147936773453, '7.2%'), (0.5208401270640535, -0.29786836361033825, '5.5%'), (0.5797918078112533, -0.1544067990567732, '2.8%'), (0.5977502755575098, -0.05190961443625878, '2.8%')]
    # plt.setp(autotexts, size=12, weight="bold")
    plt.annotate('74.3%',xy=(-1.01, 0.77),  fontsize=fontsize_det)
    plt.annotate('7.5%',xy=(-0.69, -1.02),  fontsize=fontsize_det)
    plt.annotate('7.2%',xy=(-0.13, -1.12),  fontsize=fontsize_det)
    plt.annotate('5.5%',xy=(0.3, -1.06),  fontsize=fontsize_det)
    plt.annotate('2.8%',xy=(0.6, -0.93),  fontsize=fontsize_det)
    plt.annotate('2.8%',xy=(0.76, -0.79),  fontsize=fontsize_det)
    plt.tight_layout()

    # ax.set_title("Matplotlib bakery: A pie")
    plt.savefig('K:\\python\\SQL\\images\\pie_methods.png', dpi=300) 
    # plt.show()
    
    img = Image.new('RGB', (3700, 1440), color=(255, 255, 255))
    img1 = Image.open('K:\\python\\SQL\\images\\pie_methods.png')
    img2 = Image.open('K:\\python\\SQL\\images\\oil_gas_coal.png')
    img.paste(img1, (-800,20))
    img.paste(img2, (1850,0))
    img.save("K:\\python\\SQL\\images\\methods_pie_objects.png")
    img.show()
    img.close()
  
 
def plot_hystogram_orgs():
    y_ax_label = 'No. of words/page'
    fontsize_det = 13
    conn = sqlite3.connect('SEGgrams.sqlite')
    cursor = conn.cursor()
    
    threewords = ['lateral velocity variation', 'seismic data processing', 'well log data', 'transversely isotropic medium', 'surface seismic data', 'seismic reflection data', 'shear wave velocity', 'migration velocity analysis', 'reverse time migration', 'full waveform inversion']
  
    w3_to_print = {}
    w3_leg_to_print = []

# Industry dictionaty
    conn = sqlite3.connect('SEG_affiliations_data.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SEG_affiliations_data")
    data_ind=cursor.fetchall()
    industry_dict = {}
    for element in data_ind:
        if element [0] == 'Algeria':
            break
        else:
            industry_dict[element[0]] = [i / j for i, j in zip(eval(element[1]), aver_coauth_numb_SEG)]

# count_to_print: 
# 500 < 0 element 
# 400 < 1 element <= 500
# 300 < 2 element <= 400
# 200 < 3 element <= 300
# 100 < 4 element <= 200
# 50 <  5 element <= 100
# 40 <  6 element <= 50            
# 30 <  7 element <= 40            
# 20 <  8 element <= 30            
# 10 <  9 element <= 20            
#  5 <  10 element <= 10            
#  2 <  11 element <= 5                        
#  1 <  12 element <= 2                  
#       13 element <= 1 
    small_stack1=[]
    small_stack2=[]
    small_stack3=[]
    small_stack4=[]
    small_stack5=[]
    small_stack6=[]
    small_stack7=[]
    small_stack8=[]
    small_stack9=[]
    small_stack10=[]
    small_stack11=[]
    small_stack12=[]
    small_stack13=[]
    small_stack14=[]
    
    count_to_print = zerolistmaker_1(14)

    for key, value in industry_dict.items():
        if sum(value) > 500:
            count_to_print[0] += 1
            small_stack1.append(value)            
        if sum(value) > 400 and sum(value) <= 500:
            count_to_print[1] += 1
            small_stack2.append(value)            
        if sum(value) > 300 and sum(value) <= 400:
            count_to_print[2] += 1
            small_stack3.append(value)            
        if sum(value) > 200 and sum(value) <= 300:
            count_to_print[3] += 1
            small_stack4.append(value)            
        if sum(value) > 100 and sum(value) <= 200:
            count_to_print[4] += 1
            small_stack5.append(value)            
        if sum(value) > 50 and sum(value) <= 100:
            count_to_print[5] += 1
            small_stack6.append(value)            
        if sum(value) > 40 and sum(value) <= 50:
            count_to_print[6] += 1
            small_stack7.append(value)            
        if sum(value) > 30 and sum(value) <= 40:
            count_to_print[7] += 1            
            small_stack8.append(value)
        if sum(value) > 20 and sum(value) <= 30:
            count_to_print[8] += 1
            small_stack9.append(value)
        if sum(value) > 10 and sum(value) <= 20:
            count_to_print[9] += 1
            small_stack10.append(value)
        if sum(value) > 5 and sum(value) <= 10:
            count_to_print[10] += 1
            small_stack11.append(value)
        if sum(value) > 2 and sum(value) <= 5:
            count_to_print[11] += 1
            small_stack12.append(value)
        if sum(value) > 1 and  sum(value) <= 2:
            count_to_print[12] += 1
            small_stack13.append(value)
        if sum(value) <= 1:
            count_to_print[13] += 1
            small_stack14.append(value)
            
    
    stack_of_smalls = []
    
    stack_of_smalls.append(sum_of_lists(small_stack1))
    stack_of_smalls.append(sum_of_lists(small_stack2))
    stack_of_smalls.append(sum_of_lists(small_stack3))
    stack_of_smalls.append(sum_of_lists(small_stack4))
    stack_of_smalls.append(sum_of_lists(small_stack5))
    stack_of_smalls.append(sum_of_lists(small_stack6))
    stack_of_smalls.append(sum_of_lists(small_stack7))
    stack_of_smalls.append(sum_of_lists(small_stack8))
    stack_of_smalls.append(sum_of_lists(small_stack9))
    stack_of_smalls.append(sum_of_lists(small_stack10))
    stack_of_smalls.append(sum_of_lists(small_stack11))
    stack_of_smalls.append(sum_of_lists(small_stack12))
    stack_of_smalls.append(sum_of_lists(small_stack13))
    stack_of_smalls.append(sum_of_lists(small_stack14))
    
    filewrite = open('K:\\python\\SQL\\Companies_table.txt', 'w')
    # print(sum(count_to_print) )
    list_of_ticks = ['>500', '(400:500]', '(300:400]', '(200:300]', '(100:200]', '(50:100]', '(40:50]', '(30:40]', '(20:30]', '(10:20]', '(5:10]', '(2:5]', '(1:2]', '(0:1]']
    # w3_to_print.reverse();    w2_to_print.reverse();    w1_to_print.reverse()
    # threewords.reverse();    twowords.reverse();    onewords.reverse()
    for year in range(1982, 2020):
        if year == 1982: 
            print('\t\t\t', year, sep='',  end = '\t', file = filewrite)
        else:
            print(year, end = '\t', file = filewrite)
            if year == 2019: print('', file = filewrite)
    for ii in range(0,14):
        print(list_of_ticks[ii],end = '\t', file = filewrite)
        for mm in range(0,38):
            print(round(stack_of_smalls[ii][mm], 1), end = '\t', file = filewrite)
        print('', file = filewrite)
        


    fig, ax = plt.subplots(figsize=(8,5))
    # y_pos = np.arange(len(w3_to_print.keys()))
    # plt.grid(b=None, which='minor', axis='both')
    plt.grid(which='both', axis='x', linestyle='-', linewidth=0.4)
    y_pos = list(range(14))
    ax.barh(y_pos, count_to_print, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(list_of_ticks, fontsize=fontsize_det)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of companies', fontsize=fontsize_det)
    ax.set_ylabel('Average number of papers', fontsize=fontsize_det)
    ax.set_xscale('log')
    
    plt.subplots_adjust(left=0.55, bottom=0.11, right=0.98, top=0.88, wspace=0.20, hspace=0.25)
    plt.tick_params(axis='x', labelsize=fontsize_det)
    plt.tight_layout()

    plt.savefig('K:\\python\\SQL\\images\\companies_hist.png', dpi=300)
    plt.close()
  
    
build_org_figs_all_societies()
# co_aouth_figs()
# bbb = plot_hystogram_orgs()
# bbb = pieplot()
# bbb = groups_printing3()
# bbb = groups_printing2()
# bbb = france_prod()
# bbb = plot_hystogram()
# bbb = build_org_figs()
# bbb = build_word_figs()
# bbb = groups_printing()