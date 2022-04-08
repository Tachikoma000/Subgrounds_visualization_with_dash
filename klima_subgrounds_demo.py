# Install all required libraries for the subgrounds layer
from datetime import datetime
from subgrounds.subgraph import SyntheticField, FieldPath
from subgrounds.subgrounds import Subgrounds


# instantiate subgrounds
sg = Subgrounds()
# connect to the klimaDAO subgraph API
klimaDAO = sg.load_subgraph('https://api.thegraph.com/subgraphs/name/cujowolf/klima-graph')


# ======================================================
# In this section, we construct the subgrounds synthetic fields and secondary transformations that we need for our
# dashboard
# ======================================================


# Define useful synthetic fields: Time stamp field to help with time series data analytics
klimaDAO.ProtocolMetric.datetime = SyntheticField(
  lambda timestamp: str(datetime.fromtimestamp(timestamp)),
  SyntheticField.STRING,
  klimaDAO.ProtocolMetric.timestamp,
)


# Define useful synthetic fields: Calculated metrics - sKlima Circulating supply percentage
klimaDAO.ProtocolMetric.staked_supply_percent = SyntheticField(
  lambda sklima_supply, total_supply: 100 * sklima_supply / total_supply,
  SyntheticField.FLOAT,
  [
    klimaDAO.ProtocolMetric.sKlimaCirculatingSupply,
    klimaDAO.ProtocolMetric.totalSupply
  ],
  default=100.0
)


# Use the sKlima Circ supply to generate a new variable for unstaked sKlima Circ supply
klimaDAO.ProtocolMetric.unstaked_supply_percent = 100 - klimaDAO.ProtocolMetric.staked_supply_percent


# Define useful synthetic fields: Treasury RFV per klima and ratio
klimaDAO.ProtocolMetric.rfv_per_klima = SyntheticField(
  lambda treasury_rfv, total_supply: treasury_rfv / total_supply if treasury_rfv / total_supply > 1 else 0,
  SyntheticField.FLOAT,
  [
    klimaDAO.ProtocolMetric.treasuryRiskFreeValue,
    klimaDAO.ProtocolMetric.totalSupply
  ]
)


# Use the rfv_per_klima synthetic field to generate a price_rfv_ratio metric
klimaDAO.ProtocolMetric.price_rfv_ratio = \
    100 * klimaDAO.ProtocolMetric.klimaPrice / klimaDAO.ProtocolMetric.rfv_per_klima

# Use the rfv_per_klima synthetic field to generate a Treasury market value per klima and tmv ratio
klimaDAO.ProtocolMetric.tmv_per_klima = \
    klimaDAO.ProtocolMetric.treasuryMarketValue / klimaDAO.ProtocolMetric.totalSupply
klimaDAO.ProtocolMetric.price_tmv_ratio = \
    100 * klimaDAO.ProtocolMetric.klimaPrice / klimaDAO.ProtocolMetric.tmv_per_klima


# ======================================================
# In this section, we construct the subgrounds queries
# ======================================================


# Create a function to pull immediate (latest) data points for any desired metrics you query
def immediate(sg: Subgrounds, fpath: FieldPath):
    data = sg.execute(sg.mk_request([fpath]))
    return fpath.extract_data(data)[0]


# The first query type will return the first 365 rows (days) of any field in the "protocol metrics" entity of the klima
# Subgraph
protocol_metrics_1year = klimaDAO.Query.protocolMetrics(
  orderBy=klimaDAO.ProtocolMetric.timestamp,
  orderDirection='desc',
  first=365
)


# The first query type will return the latest row of any field in the "protocol metrics" entity of the klima
# Subgraph. This is equivalent to immediate and can be used for counter type metrics or scenarios where charts
# aren't convenient
last_metric = klimaDAO.Query.protocolMetrics(
  orderBy=klimaDAO.ProtocolMetric.timestamp,
  orderDirection='desc',
  first=1
)
