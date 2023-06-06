import { Controller, Get, Inject, OnModuleInit, Param } from '@nestjs/common';
import { GrpcMethod, GrpcStreamMethod } from '@nestjs/microservices';
import { Observable } from 'rxjs';
import { HttpService, HttpModule } from '@nestjs/axios';
import { Earthquake } from './entites/earthquake.entity';
import { EarthquakeService } from '../earthquake/earthquake.service';
import { firstValueFrom } from 'rxjs';

// interface EarthquakeService {
//   createEarthquake(data: Earthquake): Observable<Earthquake>;
// }

@Controller()
export class EarthquakeController {
  constructor(
    private readonly httpService: HttpService,
    private readonly earthquakeService: EarthquakeService,
  ) {}

  @GrpcMethod('Crawler', 'Run')
  async Run(): Promise<void> {
    const { data } = await firstValueFrom(
      this.httpService.get(
        `https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=${process.env.CWB_MEMBER_AUTH_NUMBER}&limit=5&AreaName=%E6%96%B0%E7%AB%B9%E5%B8%82`,
      ),
    );

    const earthquake = await this.earthquakeService.createEarthquake(
      data.records.Earthquake[0].EarthquakeInfo.Epicenter.Location,
      data.records.Earthquake[0].EarthquakeInfo.EarthquakeMagnitude
        .MagnitudeValue,
      data.records.Earthquake[0].EarthquakeInfo.OriginTime,
    );

    console.log(data.records.Earthquake[0].EarthquakeInfo.Epicenter.Location);
    console.log(
      data.records.Earthquake[0].EarthquakeInfo.EarthquakeMagnitude
        .MagnitudeValue,
    );
    console.log(
      new Date(
        Date.parse(data.records.Earthquake[0].EarthquakeInfo.OriginTime),
      ),
    );

    return;
  }
}
