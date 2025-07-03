import click
from typing import Optional
import json
import logging
from ...timeseries.timeseries import TimeSeriesService
from ...utils.api_client import ApiClient
from json.decoder import JSONDecodeError

logger = logging.getLogger(__name__)

@click.group()
def timeseries():
    """Time series data operations"""
    pass

# Admin Time Series Operations
@timeseries.group()
def admin():
    """Admin time series operations"""
    pass

@admin.command()
@click.option('--node-id', required=True, help='Node ID to get data for')
@click.option('--param-name', required=True, help='Parameter name to get data for')
@click.option('--aggregate', help='Aggregate function (raw, latest, min, max, count, avg, sum)')
@click.option('--aggregation-interval', help='Aggregation interval (minute, hour, day, week, month, year)')
@click.option('--differential', is_flag=True, help='Apply aggregates on incremental values')
@click.option('--reset-on-negative', is_flag=True, help='Reset value if difference is negative')
@click.option('--desc-order', is_flag=True, help='Return data in descending order')
@click.option('--data-type', default='float', help='Data type (float, int, bool, string, array, object)')
@click.option('--week-start', default='Monday', help='Start day of week')
@click.option('--start-time', type=int, help='Start time in epoch seconds')
@click.option('--end-time', type=int, help='End time in epoch seconds')
@click.option('--num-intervals', type=int, help='Number of intervals to fetch')
@click.option('--start-id', help='Start ID for pagination')
@click.option('--num-records', type=int, help='Number of records to return (max 200)')
@click.option('--timezone', default='UTC', help='Timezone for query')
@click.pass_context
def tsdata(ctx, node_id: str, param_name: str, aggregate: Optional[str],
           aggregation_interval: Optional[str], differential: bool, reset_on_negative: bool,
           desc_order: bool, data_type: str, week_start: str, start_time: Optional[int],
           end_time: Optional[int], num_intervals: Optional[int], start_id: Optional[str],
           num_records: Optional[int], timezone: str):
    """Get time series data for a node as admin"""
    try:
        api_client = ctx.obj['api_client']
        timeseries_service = TimeSeriesService(api_client)
        
        result = timeseries_service.get_admin_tsdata(
            node_id=node_id,
            param_name=param_name,
            aggregate=aggregate,
            aggregation_interval=aggregation_interval,
            differential=differential,
            reset_on_negative=reset_on_negative,
            desc_order=desc_order,
            data_type=data_type,
            week_start=week_start,
            start_time=start_time,
            end_time=end_time,
            num_intervals=num_intervals,
            start_id=start_id,
            num_records=num_records,
            timezone=timezone
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error getting admin time series data: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error getting admin time series data: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@admin.command()
@click.option('--node-id', required=True, help='Node ID to get data for')
@click.option('--param-name', required=True, help='Parameter name to get data for')
@click.option('--data-type', required=True, help='Data type (float, int, bool, string, array, object)')
@click.option('--start-time', type=int, help='Start time in epoch seconds')
@click.option('--end-time', type=int, help='End time in epoch seconds')
@click.option('--start-id', help='Start ID for pagination')
@click.option('--num-records', type=int, help='Number of records to return (max 200)')
@click.pass_context
def simple_tsdata(ctx, node_id: str, param_name: str, data_type: str,
                  start_time: Optional[int], end_time: Optional[int],
                  start_id: Optional[str], num_records: Optional[int]):
    """Get simple time series data for a node as admin"""
    try:
        api_client = ctx.obj['api_client']
        timeseries_service = TimeSeriesService(api_client)
        
        result = timeseries_service.get_admin_simple_tsdata(
            node_id=node_id,
            param_name=param_name,
            data_type=data_type,
            start_time=start_time,
            end_time=end_time,
            start_id=start_id,
            num_records=num_records
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error getting admin simple time series data: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error getting admin simple time series data: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

# User Time Series Operations
@timeseries.group()
def user():
    """User time series operations"""
    pass

@user.command()
@click.option('--node-id', required=True, help='Node ID to get data for')
@click.option('--param-name', required=True, help='Parameter name to get data for')
@click.option('--aggregate', help='Aggregate function (raw, latest, min, max, count, avg, sum)')
@click.option('--aggregation-interval', help='Aggregation interval (minute, hour, day, week, month, year)')
@click.option('--differential', is_flag=True, help='Apply aggregates on incremental values')
@click.option('--reset-on-negative', is_flag=True, help='Reset value if difference is negative')
@click.option('--desc-order', is_flag=True, help='Return data in descending order')
@click.option('--data-type', default='float', help='Data type (float, int, bool, string, array, object)')
@click.option('--week-start', default='Monday', help='Start day of week')
@click.option('--start-time', type=int, help='Start time in epoch seconds')
@click.option('--end-time', type=int, help='End time in epoch seconds')
@click.option('--num-intervals', type=int, help='Number of intervals to fetch')
@click.option('--start-id', help='Start ID for pagination')
@click.option('--num-records', type=int, help='Number of records to return (max 200)')
@click.option('--timezone', default='UTC', help='Timezone for query')
@click.pass_context
def tsdata(ctx, node_id: str, param_name: str, aggregate: Optional[str],
           aggregation_interval: Optional[str], differential: bool, reset_on_negative: bool,
           desc_order: bool, data_type: str, week_start: str, start_time: Optional[int],
           end_time: Optional[int], num_intervals: Optional[int], start_id: Optional[str],
           num_records: Optional[int], timezone: str):
    """Get time series data for a node"""
    try:
        api_client = ctx.obj['api_client']
        timeseries_service = TimeSeriesService(api_client)
        
        result = timeseries_service.get_user_tsdata(
            node_id=node_id,
            param_name=param_name,
            aggregate=aggregate,
            aggregation_interval=aggregation_interval,
            differential=differential,
            reset_on_negative=reset_on_negative,
            desc_order=desc_order,
            data_type=data_type,
            week_start=week_start,
            start_time=start_time,
            end_time=end_time,
            num_intervals=num_intervals,
            start_id=start_id,
            num_records=num_records,
            timezone=timezone
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error getting time series data: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error getting time series data: {str(e)}")
        click.echo(str(e))
        raise click.Abort()

@user.command()
@click.option('--node-id', required=True, help='Node ID to get data for')
@click.option('--param-name', required=True, help='Parameter name to get data for')
@click.option('--data-type', required=True, help='Data type (float, int, bool, string, array, object)')
@click.option('--start-time', type=int, help='Start time in epoch seconds')
@click.option('--end-time', type=int, help='End time in epoch seconds')
@click.option('--start-id', help='Start ID for pagination')
@click.option('--num-records', type=int, help='Number of records to return (max 200)')
@click.pass_context
def simple_tsdata(ctx, node_id: str, param_name: str, data_type: str,
                  start_time: Optional[int], end_time: Optional[int],
                  start_id: Optional[str], num_records: Optional[int]):
    """Get simple time series data for a node"""
    try:
        api_client = ctx.obj['api_client']
        timeseries_service = TimeSeriesService(api_client)
        
        result = timeseries_service.get_user_simple_tsdata(
            node_id=node_id,
            param_name=param_name,
            data_type=data_type,
            start_time=start_time,
            end_time=end_time,
            start_id=start_id,
            num_records=num_records
        )
        click.echo(json.dumps(result, indent=2))
    except ValueError as e:
        logger.error(f"Error getting simple time series data: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
    except Exception as e:
        logger.error(f"Error getting simple time series data: {str(e)}")
        click.echo(str(e))
        raise click.Abort()
