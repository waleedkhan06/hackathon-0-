"""
CEO Briefing Generator - Generate weekly executive summaries
Part of Gold Tier AI Employee Implementation
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import json

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


class CEOBriefingGenerator:
    """
    Generate weekly CEO briefings with:
    - Task completion analysis
    - Communication metrics
    - Social media performance
    - Bottleneck identification
    - Proactive suggestions
    """

    def __init__(self, vault_path: str):
        """
        Initialize CEO Briefing Generator

        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logger = self._setup_logger()
        self.briefings_dir = self.vault_path / 'briefings'
        self.briefings_dir.mkdir(exist_ok=True)

    def _setup_logger(self) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger('CEOBriefingGenerator')
        logger.setLevel(logging.INFO)

        log_dir = self.vault_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f'ceo_briefing_{datetime.now().strftime("%Y%m%d")}.log'
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def generate_weekly_briefing(self, week_start: Optional[str] = None) -> Dict:
        """
        Generate weekly CEO briefing

        Args:
            week_start: Start date of week (YYYY-MM-DD), defaults to this week

        Returns:
            Dict with briefing info
        """
        if week_start is None:
            today = datetime.now()
            week_start = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')

        week_start_date = datetime.strptime(week_start, '%Y-%m-%d')
        week_end = (week_start_date + timedelta(days=6)).strftime('%Y-%m-%d')

        self.logger.info(f"Generating CEO briefing for week {week_start} to {week_end}")

        # Collect data
        tasks_data = self._analyze_tasks(week_start, week_end)
        communication_data = self._analyze_communication(week_start, week_end)
        social_media_data = self._analyze_social_media(week_start, week_end)
        bottlenecks = self._identify_bottlenecks(tasks_data)
        suggestions = self._generate_suggestions(tasks_data, communication_data, social_media_data)

        # Generate briefing content
        briefing_content = self._format_briefing(
            week_start, week_end, tasks_data, communication_data,
            social_media_data, bottlenecks, suggestions
        )

        # Save briefing
        briefing_file = self.briefings_dir / f'CEO_Briefing_{week_start}.md'
        briefing_file.write_text(briefing_content)

        self.logger.info(f"CEO briefing saved: {briefing_file}")

        return {
            'success': True,
            'week_start': week_start,
            'week_end': week_end,
            'briefing_file': str(briefing_file),
            'summary': {
                'tasks_completed': tasks_data['completed'],
                'tasks_pending': tasks_data['pending'],
                'bottlenecks': len(bottlenecks),
                'suggestions': len(suggestions)
            }
        }

    def _analyze_tasks(self, week_start: str, week_end: str) -> Dict:
        """Analyze task completion for the week"""
        done_dir = self.vault_path / 'done'
        needs_action_dir = self.vault_path / 'needs_action'
        pending_approval_dir = self.vault_path / 'pending_approval'

        completed_tasks = []
        pending_tasks = []
        delayed_tasks = []

        # Count completed tasks
        if done_dir.exists():
            for file in done_dir.glob('*.md'):
                try:
                    stat = file.stat()
                    modified_date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
                    if week_start <= modified_date <= week_end:
                        completed_tasks.append({
                            'name': file.stem,
                            'completed_date': modified_date
                        })
                except Exception as e:
                    self.logger.error(f"Error reading task file {file}: {e}")

        # Count pending tasks
        for folder in [needs_action_dir, pending_approval_dir]:
            if folder.exists():
                for file in folder.glob('*.md'):
                    try:
                        stat = file.stat()
                        created_date = datetime.fromtimestamp(stat.st_ctime)
                        age_days = (datetime.now() - created_date).days

                        pending_tasks.append({
                            'name': file.stem,
                            'age_days': age_days,
                            'folder': folder.name
                        })

                        # Flag as delayed if older than 3 days
                        if age_days > 3:
                            delayed_tasks.append({
                                'name': file.stem,
                                'age_days': age_days
                            })
                    except Exception as e:
                        self.logger.error(f"Error reading pending task {file}: {e}")

        return {
            'completed': len(completed_tasks),
            'pending': len(pending_tasks),
            'delayed': len(delayed_tasks),
            'completed_list': completed_tasks[:10],  # Top 10
            'pending_list': pending_tasks[:10],
            'delayed_list': delayed_tasks
        }

    def _analyze_communication(self, week_start: str, week_end: str) -> Dict:
        """Analyze communication metrics"""
        # Count emails, WhatsApp messages, LinkedIn activity
        email_count = 0
        whatsapp_count = 0
        linkedin_count = 0

        done_dir = self.vault_path / 'done'
        if done_dir.exists():
            for file in done_dir.glob('*.md'):
                try:
                    content = file.read_text()
                    if 'type: email' in content:
                        email_count += 1
                    elif 'type: whatsapp' in content:
                        whatsapp_count += 1
                    elif 'type: linkedin' in content:
                        linkedin_count += 1
                except Exception as e:
                    self.logger.error(f"Error analyzing communication file {file}: {e}")

        return {
            'emails_processed': email_count,
            'whatsapp_messages': whatsapp_count,
            'linkedin_activity': linkedin_count,
            'total_communications': email_count + whatsapp_count + linkedin_count
        }

    def _analyze_social_media(self, week_start: str, week_end: str) -> Dict:
        """Analyze social media performance"""
        # Check for social media summaries
        summaries_dir = self.vault_path / 'summaries'

        twitter_posts = 0
        facebook_posts = 0
        instagram_posts = 0
        total_engagement = 0

        if summaries_dir.exists():
            # Look for social media summary files
            for file in summaries_dir.glob('social_media_*.md'):
                try:
                    content = file.read_text()
                    # Parse metrics from summary (simplified)
                    if 'Twitter' in content:
                        twitter_posts += 1
                    if 'Facebook' in content:
                        facebook_posts += 1
                    if 'Instagram' in content:
                        instagram_posts += 1
                except Exception as e:
                    self.logger.error(f"Error reading social media summary {file}: {e}")

        return {
            'twitter_posts': twitter_posts,
            'facebook_posts': facebook_posts,
            'instagram_posts': instagram_posts,
            'total_posts': twitter_posts + facebook_posts + instagram_posts,
            'total_engagement': total_engagement
        }

    def _identify_bottlenecks(self, tasks_data: Dict) -> List[Dict]:
        """Identify bottlenecks in task processing"""
        bottlenecks = []

        # Tasks delayed more than 3 days are bottlenecks
        for task in tasks_data['delayed_list']:
            bottlenecks.append({
                'type': 'delayed_task',
                'task': task['name'],
                'age_days': task['age_days'],
                'severity': 'high' if task['age_days'] > 7 else 'medium'
            })

        # High number of pending tasks
        if tasks_data['pending'] > 20:
            bottlenecks.append({
                'type': 'high_pending_count',
                'count': tasks_data['pending'],
                'severity': 'high'
            })

        return bottlenecks

    def _generate_suggestions(self, tasks_data: Dict, communication_data: Dict,
                             social_media_data: Dict) -> List[str]:
        """Generate proactive suggestions"""
        suggestions = []

        # Task-related suggestions
        if tasks_data['delayed']:
            suggestions.append(
                f"⚠️ {tasks_data['delayed']} tasks are delayed. Consider prioritizing or delegating."
            )

        if tasks_data['pending'] > 15:
            suggestions.append(
                f"📋 High pending task count ({tasks_data['pending']}). Review and prioritize."
            )

        # Communication suggestions
        if communication_data['total_communications'] < 10:
            suggestions.append(
                "📧 Low communication activity this week. Consider reaching out to clients."
            )

        # Social media suggestions
        if social_media_data['total_posts'] < 5:
            suggestions.append(
                "📱 Social media activity is low. Aim for 8-10 posts per week across platforms."
            )

        # General suggestions
        if not suggestions:
            suggestions.append(
                "✅ All systems running smoothly. Keep up the great work!"
            )

        return suggestions

    def _format_briefing(self, week_start: str, week_end: str, tasks_data: Dict,
                        communication_data: Dict, social_media_data: Dict,
                        bottlenecks: List[Dict], suggestions: List[str]) -> str:
        """Format the CEO briefing as markdown"""

        briefing = f"""---
type: ceo_briefing
week_start: {week_start}
week_end: {week_end}
generated: {datetime.now().isoformat()}
---

# Monday Morning CEO Briefing
## Week of {week_start} to {week_end}

## Executive Summary

"""

        # Add executive summary
        if tasks_data['completed'] > tasks_data['pending']:
            briefing += "✅ **Strong week** with good task completion rate.\n"
        elif bottlenecks:
            briefing += "⚠️ **Attention needed** - bottlenecks identified.\n"
        else:
            briefing += "📊 **Steady progress** - on track with goals.\n"

        briefing += f"""
## Task Performance

- **Completed This Week**: {tasks_data['completed']}
- **Currently Pending**: {tasks_data['pending']}
- **Delayed (>3 days)**: {tasks_data['delayed']}
- **Completion Rate**: {(tasks_data['completed'] / (tasks_data['completed'] + tasks_data['pending']) * 100) if (tasks_data['completed'] + tasks_data['pending']) > 0 else 0:.1f}%

### Recently Completed Tasks
"""

        for task in tasks_data['completed_list'][:5]:
            briefing += f"- ✅ {task['name']} (completed {task['completed_date']})\n"

        if tasks_data['delayed_list']:
            briefing += "\n### ⚠️ Delayed Tasks\n"
            for task in tasks_data['delayed_list'][:5]:
                briefing += f"- 🔴 {task['name']} ({task['age_days']} days old)\n"

        briefing += f"""
## Communication Metrics

- **Emails Processed**: {communication_data['emails_processed']}
- **WhatsApp Messages**: {communication_data['whatsapp_messages']}
- **LinkedIn Activity**: {communication_data['linkedin_activity']}
- **Total Communications**: {communication_data['total_communications']}

## Social Media Performance

- **Twitter Posts**: {social_media_data['twitter_posts']}
- **Facebook Posts**: {social_media_data['facebook_posts']}
- **Instagram Posts**: {social_media_data['instagram_posts']}
- **Total Posts**: {social_media_data['total_posts']}
- **Target**: 8-10 posts/week

"""

        if bottlenecks:
            briefing += "## 🚨 Bottlenecks Identified\n\n"
            for bottleneck in bottlenecks:
                severity_emoji = "🔴" if bottleneck['severity'] == 'high' else "🟡"
                briefing += f"{severity_emoji} **{bottleneck['type'].replace('_', ' ').title()}**\n"
                if 'task' in bottleneck:
                    briefing += f"   - Task: {bottleneck['task']}\n"
                    briefing += f"   - Age: {bottleneck['age_days']} days\n"
                elif 'count' in bottleneck:
                    briefing += f"   - Count: {bottleneck['count']}\n"
                briefing += "\n"

        briefing += "## 💡 Proactive Suggestions\n\n"
        for suggestion in suggestions:
            briefing += f"- {suggestion}\n"

        briefing += f"""
## Upcoming Focus Areas

1. **Clear Delayed Tasks**: Address tasks older than 3 days
2. **Maintain Communication**: Keep response times under 24 hours
3. **Social Media Consistency**: Aim for 8-10 posts per week
4. **Review Pending Approvals**: Check `/pending_approval` folder daily

---
*🤖 Generated by AI Employee CEO Briefing System*
*Next briefing: {(datetime.strptime(week_start, '%Y-%m-%d') + timedelta(days=7)).strftime('%Y-%m-%d')}*
"""

        return briefing


def main():
    """Test the CEO Briefing Generator"""
    vault_path = os.getenv('VAULT_PATH', os.getcwd())
    generator = CEOBriefingGenerator(vault_path)

    # Generate weekly briefing
    result = generator.generate_weekly_briefing()
    print(f"Briefing generated: {result}")


if __name__ == '__main__':
    main()
