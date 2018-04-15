from boa.interop.System.ExecutionEngine import GetScriptContainer,GetExecutingScriptHash
from boa.interop.Neo.Transaction import Transaction, GetReferences, GetOutputs, GetUnspentCoins
from boa.interop.Neo.Output import GetValue, GetAssetId, GetScriptHash
from nex.np5 import *
from boa.interop.Neo.Header import GetTimestamp

neo_asset_id = b'\x9b|\xff\xda\xa6t\xbe\xae\x0f\x93\x0e\xbe`\x85\xaf\x90\x93\xe5\xfeV\xb3J\\"\x0c\xcd\xcfn\xfc3o\xc5'
gas_asset_id = b'\xe7-(iy\xeel\xb1\xb7\xe6]\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8ewX\xdeB\xe4\x16\x8bqy,`'
OnKYCRegister = RegisterAction('kyc_registration', 'address')


def get_asset_attachments(ctx):
    """
    Gets information about NEO and Gas attached to an invocation TX
    :return:
        list: A list with information about attached neo and gas
    """

    tx = GetScriptContainer()
    references = tx.References

    receiver_addr = GetExecutingScriptHash()
    sender_addr = None
    sent_amount_neo = 0
    receive_amount_token = 0

    receiver_balance = Get(ctx,receiver_addr)

    if len(references) > 0:
        reference = references[0]
        sender_addr = reference.ScriptHash
        sender_balance = Get(ctx, sender_addr)
        for output in tx.Outputs:
            if output.ScriptHash == receiver_addr:
                if output.AssetId == neo_asset_id:
                    sent_amount_neo += output.Value
                    receive_amount_token += sent_amount_neo * TOKENS_PER_NEO
                    Put(ctx, sender_addr, sender_balance + receive_amount_token)
                    Put(ctx, receiver_addr, receiver_balance - receive_amount_token)

    return [receiver_addr, sender_addr, sent_amount_neo, receive_amount_token]


def offer_lending(ctx, args):

    tx = GetScriptContainer()
    lending_key = ''
    duration = 0
    references = tx.References
    if len(references) > 0:
        reference = references[0]
        time = GetTimestamp()
        sender_addr = reference.ScriptHash
        lending_key = sender_addr + 'offer_lending'
        duration = time + args[1]

    return Put(ctx, lending_key,[args[0],duration])
