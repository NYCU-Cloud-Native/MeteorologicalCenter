import { Inject, Injectable } from '@nestjs/common';
import { IPoint } from 'influx';
import { INFLUXDB_CLIENT_TOKEN, InfluxModule } from './influx.module';
import { Point, InfluxDB } from '@influxdata/influxdb-client';

@Injectable()
export class InfluxService {
  constructor(
    @Inject('INFLUXDB_CLIENT_TOKEN')
    private readonly influxclient: InfluxDB,
  ) {}

  public async writeRecord(data: Point) {
    await this.influxclient
      .getWriteApi(process.env.INFLUX_ORG, process.env.INFLUX_BUCKET, 's')
      .writePoint(data);
  }
}
