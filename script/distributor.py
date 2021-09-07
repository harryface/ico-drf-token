from django.db import transaction

from main.models import Bid, SiteConfiguration, SuccessfulBid, UnSuccessfulBid


def assign_partial(_bids, token, site_config):
    assigned_list = []
    for_all = token // len(_bids)
    remainder = token % for_all
    for index, bid in enumerate(_bids):
        # assign to the first _bids
        if index < remainder:
            assigned_list.append(
                SuccessfulBid(
                    bid_id=bid['id'],
                    token_allotted=(for_all+1)
                )
            )
        else:
            assigned_list.append(
                SuccessfulBid(
                    bid_id=bid['id'],
                    token_allotted=for_all
                )
            )
    try:
        with transaction.atomic():
            SuccessfulBid.objects.bulk_create(assigned_list)

            site_config.available_token = 0
            site_config.distributed = True
            site_config.save(
                update_fields=[
                    'available_token',
                    'distributed'
                ]
            )

    except:
        transaction.rollback()

    return


def assign_whole(_bids, total_in_set, site_config):
    # bulk create this and subtract from token too
    try:
        with transaction.atomic():
            SuccessfulBid.objects.bulk_create(
                [
                    SuccessfulBid(
                        bid_id=bid['id'],
                        token_allotted=bid['number_of_tokens']
                    ) for bid in _bids
                ]
            )

            site_config.available_token -= total_in_set
            site_config.save(
                update_fields=['available_token', ]
            )

    except:
        transaction.rollback()

    return


def unsuccessful_assign(_bids):
    # bulk create the unassign objects
    UnSuccessfulBid.objects.bulk_create(
        [UnSuccessfulBid(bid_id=bid['id'],) for bid in _bids]
    )

    return


def start():
    site_config = SiteConfiguration.objects.filter(distributed=False).first()

    if not site_config:
        return

    bids = Bid.objects.all().filter(
        created_at__lte=site_config.end_date,
        created_at__gte=site_config.start_date
    ).order_by('-unit_price', 'created_at').values()

    bids_count = len(bids)

    token = site_config.available_token
    # set to amount of first entity at init
    total_in_set = bids[0]['number_of_tokens']

    i = 0
    j = 1
    while True:
        # if available token & not end of bid
        if token and (j < bids_count):
            # check if same price bracket, then add token number to total set
            if bids[i]['unit_price'] == bids[j]['unit_price']:
                total_in_set += bids[j]['number_of_tokens']
            # if not same, move into here
            else:
                # if enough token, assign whole
                if token > total_in_set:
                    assign_whole(bids[i:j], total_in_set, site_config)
                    token -= total_in_set
                # else assign partial and break
                else:
                    assign_partial(bids[i:j], token, site_config)
                    unsuccessful_assign(bids[j:])
                    token = 0
                    break
                # set i to new instance, and increment j
                i = j
                total_in_set = bids[i]['number_of_tokens']

            j += 1
        else:
            break

    return
