"""报告生成模块
功能：
1. 施工日报生成
2. 周报/月报模板
3. 质量报告汇总
4. 进度报告
5. HTML/PDF格式输出
"""

from datetime import datetime, timedelta

class ReportSystem:
    """报告生成系统"""
    
    def __init__(self):
        self.data = {
            'daily': [],
            'quality': [],
            'progress': [],
            'weather': [],
            'issues': []
        }
    
    # === 日报 ===
    def add_daily_record(self, date, mileage, work_type, workers, equipment, weather, notes=""):
        """添加日报记录"""
        record = {
            'date': date,
            'mileage': mileage,
            'work_type': work_type,
            'workers': workers,
            'equipment': equipment,
            'weather': weather,
            'notes': notes
        }
        self.data['daily'].append(record)
        return record
    
    def generate_daily(self, date=None):
        """生成日报"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        records = [r for r in self.data['daily'] if r['date'] == date]
        
        if not records:
            return f"{date} 无施工记录"
        
        report = []
        report.append("="*60)
        report.append(f"施工日报 - {date}")
        report.append("="*60)
        
        for r in records:
            report.append(f"\n里程: K{r['mileage']}")
            report.append(f"施工类型: {r['work_type']}")
            report.append(f"人员: {r['workers']}人")
            report.append(f"设备: {r['equipment']}")
            report.append(f"天气: {r['weather']}")
            if r['notes']:
                report.append(f"备注: {r['notes']}")
        
        return "\n".join(report)
    
    # === 周报 ===
    def generate_weekly(self, week_start=None):
        """生成周报"""
        if week_start is None:
            week_start = datetime.now() - timedelta(days=7)
        
        week_end = week_start + timedelta(days=6)
        
        # 收集本周数据
        daily_records = []
        for d in range(7):
            date = (week_start + timedelta(days=d)).strftime('%Y-%m-%d')
            records = [r for r in self.data['daily'] if r['date'] == date]
            daily_records.extend(records)
        
        report = []
        report.append("="*60)
        report.append(f"周报 - {week_start.strftime('%Y-%m-%d')} 至 {week_end.strftime('%Y-%m-%d')}")
        report.append("="*60)
        
        # 施工天数
        report.append(f"\n施工天数: {len(set(r['date'] for r in daily_records))}/7")
        
        # 汇总
        if daily_records:
            total_workers = sum(r['workers'] for r in daily_records)
            report.append(f"累计人员: {total_workers}人次")
        
        # 问题汇总
        issues = [i for i in self.data['issues'] 
                 if week_start.strftime('%Y-%m-%d') <= i['date'] <= week_end.strftime('%Y-%m-%d')]
        report.append(f"\n问题数: {len(issues)}")
        for i in issues:
            report.append(f"  - {i['date']}: {i['description']}")
        
        return "\n".join(report)
    
    # === 月报 ===
    def generate_monthly(self, year=None, month=None):
        """生成月报"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        month_str = f"{year}-{month:02d}"
        
        # 收集本月数据
        records = [r for r in self.data['daily'] if r['date'].startswith(month_str)]
        
        report = []
        report.append("="*60)
        report.append(f"月报 - {year}年{month}月")
        report.append("="*60)
        
        # 统计
        days_worked = len(set(r['date'] for r in records))
        total_workers = sum(r['workers'] for r in records)
        
        report.append(f"\n工作天数: {days_worked}天")
        report.append(f"累计人员: {total_workers}人次")
        
        # 施工类型统计
        work_types = {}
        for r in records:
            wt = r['work_type']
            work_types[wt] = work_types.get(wt, 0) + 1
        
        report.append("\n施工类型统计:")
        for wt, count in work_types.items():
            report.append(f"  {wt}: {count}次")
        
        return "\n".join(report)
    
    # === 质量报告 ===
    def add_quality_record(self, date, mileage, item, result, status, inspector=""):
        """添加质量记录"""
        record = {
            'date': date,
            'mileage': mileage,
            'item': item,
            'result': result,
            'status': status,
            'inspector': inspector
        }
        self.data['quality'].append(record)
        return record
    
    def generate_quality_report(self, start_date=None, end_date=None):
        """生成质量报告"""
        records = self.data['quality']
        
        if start_date:
            records = [r for r in records if r['date'] >= start_date]
        if end_date:
            records = [r for r in records if r['date'] <= end_date]
        
        report = []
        report.append("="*60)
        report.append("质量检查报告")
        report.append("="*60)
        
        total = len(records)
        ok = len([r for r in records if r['status'] == 'ok'])
        warning = len([r for r in records if r['status'] == 'warning'])
        
        report.append(f"\n总计: {total}项")
        report.append(f"合格: {ok}项 ({ok/total*100:.0f}%)" if total > 0 else "合格: 0项")
        report.append(f"警告: {warning}项" if warning > 0 else "")
        
        report.append("\n详细记录:")
        for r in records:
            icon = "✅" if r['status'] == 'ok' else "⚠️"
            report.append(f"  {icon} K{r['mileage']}: {r['item']} = {r['result']}")
        
        return "\n".join(report)
    
    # === 进度报告 ===
    def add_progress_record(self, mileage_start, mileage_end, status, percent, date=None):
        """添加进度记录"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        record = {
            'date': date,
            'start': mileage_start,
            'end': mileage_end,
            'status': status,
            'percent': percent
        }
        self.data['progress'].append(record)
        return record
    
    def generate_progress_report(self):
        """生成进度报告"""
        report = []
        report.append("="*60)
        report.append("施工进度报告")
        report.append("="*60)
        
        # 按状态统计
        statuses = {}
        for p in self.data['progress']:
            s = p['status']
            if s not in statuses:
                statuses[s] = []
            statuses[s].append(p)
        
        for status, records in statuses.items():
            total_percent = sum(p['percent'] for p in records)
            avg_percent = total_percent / len(records) if records else 0
            report.append(f"\n【{status}】")
            report.append(f"  段数: {len(records)}")
            report.append(f"  平均进度: {avg_percent:.1f}%")
        
        # 总体进度
        all_progress = [p['percent'] for p in self.data['progress']]
        if all_progress:
            overall = sum(all_progress) / len(all_progress)
            report.append(f"\n总体进度: {overall:.1f}%")
        
        return "\n".join(report)
    
    # === 添加问题 ===
    def add_issue(self, date, description, severity, resolution=""):
        """添加问题记录"""
        record = {
            'date': date,
            'description': description,
            'severity': severity,
            'resolution': resolution
        }
        self.data['issues'].append(record)
        return record
    
    # === HTML导出 ===
    def export_html(self, title="施工报告", content=""):
        """导出HTML"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .ok {{ color: green; }}
        .warning {{ color: orange; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    {content}
</body>
</html>
"""
        return html


# 测试
if __name__ == "__main__":
    rs = ReportSystem()
    
    # 添加日报
    rs.add_daily_record('2026-02-28', 1.5, '沥青摊铺', 15, '压路机2台', '晴天')
    rs.add_daily_record('2026-02-27', 1.2, '水稳层', 12, '摊铺机1台', '多云')
    
    # 添加质量记录
    rs.add_quality_record('2026-02-28', 1.5, '压实度', '98%', 'ok', '张三')
    rs.add_quality_record('2026-02-27', 1.2, '温度', '145°C', 'ok', '李四')
    
    # 添加进度
    rs.add_progress_record(0, 1, '已完成', 100)
    rs.add_progress_record(1, 2, '进行中', 70)
    
    # 添加问题
    rs.add_issue('2026-02-28', '压路机故障', 'medium', '已修复')
    
    # 输出报告
    print(rs.generate_daily())
    print()
    print(rs.generate_progress_report())
    print()
    print(rs.generate_quality_report())
