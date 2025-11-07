"""
SSE Manager - Server-Sent Events Yönetimi
- Message queue yönetimi
- Real-time bildirimler
"""

import queue

class SSEManager:
    def __init__(self):
        # User ID bazlı message queue'lar
        self.message_queues = {}
    
    def create_queue(self, user_id):
        """Kullanıcı için queue oluştur"""
        if user_id not in self.message_queues:
            self.message_queues[user_id] = queue.Queue(maxsize=100)
        return self.message_queues[user_id]
    
    def get_queue(self, user_id):
        """Kullanıcının queue'sunu getir"""
        return self.message_queues.get(user_id)
    
    def notify(self, user_id, message_data):
        """Kullanıcıya mesaj gönder"""
        if user_id in self.message_queues:
            try:
                self.message_queues[user_id].put(message_data, block=False)
                return True
            except queue.Full:
                return False
        return False
    
    def remove_queue(self, user_id):
        """Queue'yu kaldır"""
        if user_id in self.message_queues:
            del self.message_queues[user_id]
    
    def get_stats(self):
        """İstatistikler"""
        return {
            'active_connections': len(self.message_queues),
            'total_queued': sum(q.qsize() for q in self.message_queues.values())
        }

# Global SSE manager instance
sse_manager = SSEManager()
