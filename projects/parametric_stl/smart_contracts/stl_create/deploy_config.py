import logging
from pathlib import Path
import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk import account, encoding
import base64
import random

from algokit_utils import (
    Account,
    ApplicationSpecification,
    EnsureBalanceParameters,
    transfer,
    Account,
    EnsureBalanceParameters,
    TransactionParameters,
    TransferParameters,
    CreateTransactionParameters,
    ensure_funded,
    get_account,
)
from algosdk.util import algos_to_microalgos

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
    deployer_initial_funds: int = 20,
) -> None:
    from smart_contracts.artifacts.stl_create.client import (
        ParametricStlClient,
    )

    app_client = ParametricStlClient(
        algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )

    app_client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )

    transfer(
        algod_client,
        TransferParameters(
            from_account=deployer,
            to_address=app_client.app_address,
            micro_algos=100_000_000,
        ),
    )

    dna = 2500
    dna = 18446744073709551615
    dna = random.randint(0,18446744073709551615)
    response = app_client.create_stl(dna=dna, transaction_parameters=CreateTransactionParameters(boxes=[(0, "stl"), (0, ""), (0, ""), (0, ""), (0, ""), (0, ""), (0, ""), (0, "")]))
    logger.info(
        f"Called hello on ({app_client.app_id}) "
        f"with dna value ={dna}, received: {response.return_value}"
    )


    index = app_client.app_id
    boxName = b'stl'
    print('Querying application id: %s' %(index))
    print('Querying box name: %s' %(boxName))
    boxNames = algod_client.application_boxes(index)
    print('Application id: %s has box with name %s' %(index, boxNames))
    boxResponse = algod_client.application_box_by_name(index, boxName)
    boxValue = boxResponse['value']
    stl_string = base64.b64decode(boxValue)[0:].decode('utf8')
    # print(stl_string)
    file = open("head.stl", "w")
    file.write(stl_string)
    file.close()
