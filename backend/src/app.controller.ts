import { Controller, Post, Get, Body, Param, HttpCode } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Post('blinks/:userId')
  @HttpCode(201)
  async saveBlinks(@Param('userId') userId: string, @Body() blinks: any[]) {
    return this.appService.saveBlinks(userId, blinks);
  }

  @Get('dashboard/:userId')
  async getDashboard(@Param('userId') userId: string) {
    return this.appService.getDashboard(userId);
  }
}
