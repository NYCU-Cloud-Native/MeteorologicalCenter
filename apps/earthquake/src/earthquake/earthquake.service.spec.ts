import { Test, TestingModule } from '@nestjs/testing';
import { EarthquakeService } from './earthquake.service';
import { EarthquakeController } from './earthquake.controller';
import { Provider } from '@nestjs/common';
import { InfluxService } from '../influx/influx.service';
import { Point } from '@influxdata/influxdb-client';
import { HttpModule, HttpService } from '@nestjs/axios';

describe('EarthquakeService', () => {
  let earthquakeService: EarthquakeService;
  let httpService: HttpService;
  let earthquakeController: EarthquakeController;
  let influxService = {
    writeRecord: jest.fn(),
  } as unknown as InfluxService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      imports: [ HttpModule ],
      controllers: [ EarthquakeController ],
      providers: [
        EarthquakeService,
        {
          provide: InfluxService,
          useValue: influxService,
        } as Provider,
      ],
    }).compile();

    earthquakeService = module.get<EarthquakeService>(EarthquakeService);
    earthquakeController = module.get<EarthquakeController>(EarthquakeService);
  });

  describe('writeRecord', () => {
    it('should return null',
      async () => {
        const result = null;
        const parameter = {
          Epicenter: 'Tainan',
          MagnitudeValue: 3.0,
          OriginTime: new Date('Sat May 13 2023 01:30:20 GMT+0800'),
        };

        jest
          .spyOn(influxService, 'writeRecord')
          .mockImplementation(() => result);

        await earthquakeService.createEarthquake(
          parameter.Epicenter,
          parameter.MagnitudeValue,
          parameter.OriginTime,
        );

        expect(influxService.writeRecord).toBeCalledWith(
          new Point('earthquake')
            .tag('Epicenter', parameter.Epicenter)
            .floatField('MagnitudeValue', parameter.MagnitudeValue)
            .timestamp(parameter.OriginTime),
        );
      });
  });

  // it('should be defined', () => {
  //   expect(earthquakeService).toBeDefined();
  // });
});
