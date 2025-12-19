import { AppService } from './app.service';
export declare class AppController {
    private readonly appService;
    constructor(appService: AppService);
    saveBlinks(userId: string, blinks: any[]): Promise<{
        success: boolean;
        saved: number;
    }>;
    getDashboard(userId: string): Promise<{
        totalBlinks: number;
        avgBlinksPerHour: number;
        data: {
            time: string;
            blinks: number;
        }[];
    }>;
}
