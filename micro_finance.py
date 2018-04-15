from nex.txio import *
from nex.txio import get_asset_attachments
from nex.np5 import *
from boa.interop.Neo.Storage import Get, Put
from boa.interop.Neo.Action import RegisterAction


KYC_KEY = b'kyc_ok'
OK_COUNT = 'ok_count'
OnRefund = RegisterAction('refund', 'addr_to', 'amount')

ctx = GetContext()
NEP5_METHODS = ['name', 'symbol', 'decimals', 'totalSupply', 'balanceOf', 'transfer', 'transferFrom', 'approve', 'allowance']


def Main(operation, args):
    """
    :param operation: str The name of the operation to perform
    :param args: list A list of arguments along with the operation
    :return:
        bytearray: The result of the operation
    """
        # the following are handled by crowdsale
    if operation == 'kyc_register':
        return kyc_reg(ctx, args)
    elif operation == 'offer_lending':
        return offer_lending(ctx, args)
    elif operation == 'get_attachments':
        return get_asset_attachments(ctx)

    for op in NEP5_METHODS:
            if operation == op:
                return handle_nep51(ctx, operation, args)

    return 'unknown operation'


def kyc_reg(ctx, args):
    ok_count = Get(ctx,OK_COUNT)
    address = args
    if len(address) == 20:
        kyc_storage_key = concat(KYC_KEY, address)
        Put(ctx, kyc_storage_key, True)
        ok_count += 1

    return Put(ctx,OK_COUNT,ok_count)

