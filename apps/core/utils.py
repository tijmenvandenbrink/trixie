import logging

logger = logging.getLogger(__name__)


def mkdate(datestring):
    """ Return a datetime object from string

        :param datestring: date string in the form of YYYY-MM-DD
        :type datestring: string
        :returns: datetime object
    """
    from datetime import datetime
    from django.utils.timezone import utc
    import re

    if re.match('\d{4}-\d{1,2}-{1,2}', datestring):
        return datetime.strptime(datestring, '%Y-%m-%d').replace(tzinfo=utc)
    elif re.match('\d{4}-\d{1,2}', datestring):
        return datetime.strptime(datestring, '%Y-%m').replace(tzinfo=utc)


def overlap(l1, l2):
    """
        Look for overlapping intervals between two lists.
        Each list consist of lists with a start and end datetime objects:
                 [(start, end), (start, end), ....]
        Any or both lists may be empty.

        A1       e1[0]------e1[1]                               e1[0] <= e2[0] and e1[1] <= e2[0]
                                    e2[0]------e2[1]
                                                                      OR
        A2                          e1[0]------e1[1]            e1[0] >= e2[1] and e1[1] >= e2[1]
                 e2[0]------e2[1]


        B1       e1[0]------e1[1]                               e1[0] <= e2[0] and e1[1] <= e2[1]
                        e2[0]------e2[1]
                                                                      OR
        B2              e1[0]------e1[1]                        e1[0] >= e2[0] and e1[1] >= e2[1]
                 e2[0]------e2[1]


        C1       e1[0]--------------------e1[1]                 e1[0] <= e2[0] and e1[1] >= e2[1]
                       e2[0]------e2[1]
                                                                         OR
        C2              e1[0]-----e1[1]                         e1[0] >= e2[0] and e1[1] <= e2[1]
                   e2[0]---------------------e2[1]

        Situation A1 -> No overlap
        Situation A2 -> No overlap

        Situation B1 -> start = e2[0], end = e1[1]
        Situation B2 -> start = e1[0], end = e2[1]

        Situation C1 -> start = e2[0], end = e2[1]
        Situation C2 -> start = e1[0], end = e1[1]

        :param l1: List of start, end tuples. [(start, end), (start, end), ....]
        :type l1: list
        :param l2: List of start, end tuples. [(start, end), (start, end), ....]
        :type l2: list
        :returns: list of start, end tuples. [(start, end), (start, end), ....]
    """
    result = []
    for e1 in l1:
        for e2 in l2:
            if (e1[0] <= e2[0] and e1[1] <= e2[0]) or (e1[0] >= e2[1] and e1[1] >= e2[1]):  #A1 and A2
                continue
            elif e1[0] <= e2[0] and e1[1] <= e2[1]:                                         #B1
                start = e2[0]
                end = e1[1]
            elif e1[0] >= e2[0] and e1[1] >= e2[1]:                                         #B2
                start = e1[0]
                end = e2[1]
            elif e1[0] <= e2[0] and e1[1] >= e2[1]:                                         #C1
                start = e2[0]
                end = e2[1]
            elif e1[0] >= e2[0] and e1[1] <= e2[1]:                                         #C2
                start = e1[0]
                end = e1[1]
            else:
                return result

            result.append((start, end))

    return result


def calculate_availability(start, end, duration):
    """
        Return availability percentage
        start, end are datetime objects and represents the period
        over which the availability should be calculated.
        duration is a timedelta object
    """
    total = end - start
    result = (1.0 - (duration.total_seconds() / total.total_seconds())) * 100

    return result


def update_obj(obj, **kwargs):
    """ Updates an object with kwargs and returns the object

    :param obj: Object
    :type obj: Object
    :return: Object
    """
    for k, v in kwargs.items():
        if not getattr(obj, k) == v:
            logger.info('action="Object update", status="OK", object_id="{obj.id}", object="{obj}", '
                        'attribute="{attribute}", oldvalue="{oldvalue}", '
                        'newvalue="{newvalue}"'.format(obj=obj, attribute=k, oldvalue=getattr(obj, k), newvalue=v))
            setattr(obj, k, v)
    obj.save()
    return obj