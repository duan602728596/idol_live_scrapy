import './sourcemap.mjs';
import * as process from 'node:process';
import { spawn, type ChildProcess, type SpawnOptions } from 'node:child_process';
import { join } from 'node:path';
import { CronJob } from 'cron';
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn.js';
import { metaHelper } from '@sweet-milktea/utils';

dayjs.locale('zh-cn');

const { __dirname }: { __dirname: string } = metaHelper(import.meta.url);
const isWindows: boolean = process.platform === 'win32';

/* 路径 */
const python: string = join(__dirname, '../.venv/Scripts/python.exe');
const scrapy: string = join(__dirname, '../.venv/Scripts/scrapy.exe');
const liveSpider: string = join(__dirname, '../src/weibo_idol_live');

/**
 * 执行命令
 * @param { string } cmd - 命令
 * @param { Array<string> } args - 参数
 * @param { string } cwdPath - 文件夹
 */
export function command(cmd: string, args: Array<string>, cwdPath: string): Promise<void> {
  return new Promise((resolve: Function, reject: Function): void => {
    const spawnOptions: SpawnOptions = {
      stdio: 'inherit',
      cwd: cwdPath
    };

    if (isWindows) spawnOptions.shell = true;

    const child: ChildProcess = spawn(cmd, args, spawnOptions);

    child.on('close', function(code: number | null): void {
      resolve();
    });

    child.on('error', function(error: Error): void {
      reject(error);
    });
  });
}

/* 爬虫 */
CronJob.from({
  cronTime: '0 0 9,17,22 * * *',
  async onTick(): Promise<void> {
    console.log(`[${ dayjs().format('YYYY-MM-DD HH:mm:ss') }]开始执行爬虫任务。`);
    await command(scrapy, ['crawl', 'live_spider', '-L', 'WARNING'], liveSpider);
    console.log(`[${ dayjs().format('YYYY-MM-DD HH:mm:ss') }]爬虫任务执行完毕。`);
  },
  start: true
});

/* 删除过期数据 */
CronJob.from({
  cronTime: '0 0 0 1 * *',
  async onTick(): Promise<void> {
    console.log(`[${ dayjs().format('YYYY-MM-DD HH:mm:ss') }]开始执行过期数据清理任务。`);
    await command(python, ['src/cron/clear_expiration.py'], join(__dirname, '..'));
    console.log(`[${ dayjs().format('YYYY-MM-DD HH:mm:ss') }]过期数据清理任务执行完毕。`);
  },
  start: true
});

/* 删除过期爬虫日志文件 */
CronJob.from({
  cronTime: '0 0 3 1 * *',
  async onTick(): Promise<void> {
    console.log(`[${ dayjs().format('YYYY-MM-DD HH:mm:ss') }]开始执行爬虫日志文件清理任务。`);
    await command(python, ['src/cron/clear_log.py'], join(__dirname, '..'));
    console.log(`[${ dayjs().format('YYYY-MM-DD HH:mm:ss') }]爬虫日志文件清理任务执行完毕。`);
  },
  start: true
});

/* 删除过期日志记录文件 */
CronJob.from({
  cronTime: '0 0 5 1 * *',
  async onTick(): Promise<void> {
    console.log(`[${ dayjs().format('YYYY-MM-DD HH:mm:ss') }]开始执行日志记录清理任务。`);
    await command(python, ['src/cron/clear_log_db.py'], join(__dirname, '..'));
    console.log(`[${ dayjs().format('YYYY-MM-DD HH:mm:ss') }]日志记录清理任务执行完毕。`);
  },
  start: true
});