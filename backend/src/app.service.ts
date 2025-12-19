import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  async saveBlinks(userId: string, blinks: any[]) {
    console.log(`📊 Saving ${blinks.length} blinks for user ${userId}`);
    blinks.forEach(blink => {
      console.log(`  Blink #${blink.count} at ${new Date(blink.timestamp * 1000).toISOString()}`);
    });
    return { success: true, saved: blinks.length };
  }

  async getDashboard(userId: string) {
    return {
      totalBlinks: 127,
      avgBlinksPerHour: 23,
      data: [{ time: '10:00', blinks: 12 }]
    };
  }
}
